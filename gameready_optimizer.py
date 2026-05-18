bl_info = {
    "name": "GameReady Optimizer",
    "author": "Kuzey Kayra Eyioğlu",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > GameReady",
    "description": "Analyze and optimize selected objects for game engines",
    "category": "Object",
}

import bpy
import bmesh


def selected_mesh_objects():
    return [obj for obj in bpy.context.selected_objects if obj.type == "MESH"]


def count_object_tris(obj):
    tris = 0
    for poly in obj.data.polygons:
        tris += max(len(poly.vertices) - 2, 1)
    return tris


class GROPERTIES(bpy.types.PropertyGroup):
    triangle_count: bpy.props.IntProperty(default=0)
    estimated_lod_tris: bpy.props.IntProperty(default=0)
    object_count: bpy.props.IntProperty(default=0)
    material_count: bpy.props.IntProperty(default=0)

    lod1_quality: bpy.props.FloatProperty(
        name="LOD1 Quality",
        default=0.80,
        min=0.05,
        max=1.0
    )

    lod2_quality: bpy.props.FloatProperty(
        name="LOD2 Quality",
        default=0.55,
        min=0.05,
        max=1.0
    )

    lod3_quality: bpy.props.FloatProperty(
        name="LOD3 Quality",
        default=0.30,
        min=0.05,
        max=1.0
    )

    lod_spacing: bpy.props.FloatProperty(
        name="LOD Spacing",
        default=1.4,
        min=1.0,
        max=5.0
    )

    low_poly_warning: bpy.props.BoolProperty(default=False)


class GAME_READY_OT_analyze(bpy.types.Operator):
    bl_idname = "gameready.analyze"
    bl_label = "Analyze Selected"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = selected_mesh_objects()
        props = context.scene.gameready_props

        total_tris = 0
        materials = set()

        for obj in objs:
            total_tris += count_object_tris(obj)

            for mat in obj.data.materials:
                if mat:
                    materials.add(mat.name)

        props.object_count = len(objs)
        props.triangle_count = total_tris
        props.material_count = len(materials)

        props.estimated_lod_tris = int(
            total_tris * (
                props.lod1_quality +
                props.lod2_quality +
                props.lod3_quality
            )
        )

        props.low_poly_warning = total_tris < 300

        self.report({"INFO"}, "Analysis complete")
        return {"FINISHED"}


class GAME_READY_OT_safe_optimize(bpy.types.Operator):
    bl_idname = "gameready.safe_optimize"
    bl_label = "Safe Optimize"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = selected_mesh_objects()

        if not objs:
            self.report({"WARNING"}, "No mesh object selected")
            return {"CANCELLED"}

        for obj in objs:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj

            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            mesh = obj.data
            bm = bmesh.new()
            bm.from_mesh(mesh)

            loose_verts = [v for v in bm.verts if not v.link_edges]
            if loose_verts:
                bmesh.ops.delete(bm, geom=loose_verts, context="VERTS")

            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)

            bm.to_mesh(mesh)
            bm.free()
            mesh.update()

            for i in reversed(range(len(obj.material_slots))):
                if obj.material_slots[i].material is None:
                    obj.active_material_index = i
                    bpy.ops.object.material_slot_remove()

        self.report({"INFO"}, "Safe optimization complete")
        return {"FINISHED"}


class GAME_READY_OT_create_lods(bpy.types.Operator):
    bl_idname = "gameready.create_lods"
    bl_label = "Create Better LODs"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        objs = selected_mesh_objects()
        props = context.scene.gameready_props

        if not objs:
            self.report({"WARNING"}, "No mesh object selected")
            return {"CANCELLED"}

        lod_settings = [
            ("LOD1", props.lod1_quality, 1),
            ("LOD2", props.lod2_quality, 2),
            ("LOD3", props.lod3_quality, 3),
        ]

        original_selection = objs.copy()

        for obj in original_selection:
            original_tris = count_object_tris(obj)

            if original_tris < 300:
                self.report(
                    {"WARNING"},
                    f"{obj.name} is already low poly. LODs may not look useful."
                )

            object_width = max(obj.dimensions.x, obj.dimensions.y, 1.0)
            spacing = object_width * props.lod_spacing

            obj.name = obj.name.replace("_LOD0", "")
            obj.name = f"{obj.name}_LOD0"

            for lod_name, ratio, spacing_multiplier in lod_settings:
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()

                base_name = obj.name.replace("_LOD0", "")
                new_obj.name = f"{base_name}_{lod_name}"
                new_obj.data.name = f"{base_name}_{lod_name}_Mesh"

                context.collection.objects.link(new_obj)

                new_obj.location.x += spacing * spacing_multiplier

                decimate = new_obj.modifiers.new(
                    name=f"{lod_name}_Decimate",
                    type="DECIMATE"
                )
                decimate.ratio = ratio
                decimate.use_collapse_triangulate = True

                bpy.ops.object.select_all(action="DESELECT")
                new_obj.select_set(True)
                bpy.context.view_layer.objects.active = new_obj

                try:
                    bpy.ops.object.modifier_apply(modifier=decimate.name)
                except Exception:
                    self.report({"WARNING"}, f"Could not apply Decimate on {new_obj.name}")

                new_obj.select_set(False)

        bpy.ops.object.select_all(action="DESELECT")

        for obj in original_selection:
            obj.select_set(True)

        context.view_layer.objects.active = original_selection[0]

        self.report({"INFO"}, "Better LODs created")
        return {"FINISHED"}


class GAME_READY_PT_panel(bpy.types.Panel):
    bl_label = "GameReady Optimizer"
    bl_idname = "GAME_READY_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "GameReady"

    def draw(self, context):
        layout = self.layout
        props = context.scene.gameready_props

        layout.label(text="Analysis", icon="VIEWZOOM")
        layout.operator("gameready.analyze", icon="VIEWZOOM")

        box = layout.box()
        box.label(text=f"Objects: {props.object_count}")
        box.label(text=f"Triangles: {props.triangle_count}")
        box.label(text=f"Materials: {props.material_count}")
        box.label(text=f"Estimated LOD Tris: {props.estimated_lod_tris}")

        if props.low_poly_warning:
            warning_box = layout.box()
            warning_box.label(text="Low Poly Warning", icon="ERROR")
            warning_box.label(text="LOD may not be useful.")

        layout.separator()

        layout.label(text="Safe Optimization", icon="CHECKMARK")
        layout.operator("gameready.safe_optimize", icon="CHECKMARK")

        layout.separator()

        layout.label(text="Better LOD Settings", icon="MOD_DECIM")

        lod_box = layout.box()
        lod_box.prop(props, "lod1_quality")
        lod_box.prop(props, "lod2_quality")
        lod_box.prop(props, "lod3_quality")
        lod_box.prop(props, "lod_spacing")

        layout.operator("gameready.create_lods", icon="MOD_DECIM")


classes = (
    GROPERTIES,
    GAME_READY_OT_analyze,
    GAME_READY_OT_safe_optimize,
    GAME_READY_OT_create_lods,
    GAME_READY_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.gameready_props = bpy.props.PointerProperty(type=GROPERTIES)


def unregister():
    del bpy.types.Scene.gameready_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
