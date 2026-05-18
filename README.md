# GameReady Optimizer

<p align="center">
  <a href="showcase_result.png">
    <img src="showcase_click.png" width="900"/>
  </a>
</p>

<p align="center">
<i>Click the image to see the result</i>
</p>

<p align="center">
Optimize Blender models for Unity & Unreal Engine in one click.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v1.0.0-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Blender-4.0%2B-E87D0D?style=for-the-badge&logo=blender&logoColor=white"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-100%25-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
</p>

<p align="center">
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/blender/blender-original.svg" width="50"/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50"/>
</p>


---

## About

GameReady Optimizer is a Blender add-on designed to help game developers optimize 3D models for game engines.

It allows you to analyze meshes, create smart LODs, and safely optimize models while keeping the workflow simple.

Perfect for:

- Unity projects
- Unreal Engine projects
- Environment assets
- Props
- Characters
- Large scenes

---

## Downloads

### Latest Version (Recommended)

⬇️ **[Download GameReady Optimizer v1.0.0](../../releases/tag/v1.0.0)**

Supports:

- Blender 4.0+
- Python (Included with Blender)

---

## Features

### Smart LOD Generation
Automatically creates:

```text
LOD0
LOD1
LOD2
LOD3
```

### Safe Optimize
Safely performs:

```text
Apply Rotation
Apply Scale
Fix Normals
Remove Loose Vertices
Remove Empty Material Slots
```

### Low Poly Detection
Warns you when an object is already low poly.

---

## Example Result

<p align="center">
  <img src="showcase_result.png" width="900"/>
</p>

Example:

```text
48,918 triangles → 4,890 triangles
~90% triangle reduction while preserving shape
```

while still preserving the overall shape.

---

## Installation

1. Download the `.py` file

2. Open Blender

```text
Edit → Preferences → Add-ons → Install
```

3. Select:

```text
gameready_optimizer.py
```

4. Enable the add-on

5. Open:

```text
N Panel → GameReady
```

---

## How To Use

1. Select your mesh object

2. Click:

```text
Analyze Selected
```

3. Adjust:

```text
LOD1 Quality
LOD2 Quality
LOD3 Quality
LOD Spacing
```

4. Click:

```text
Create Better LODs
```

---

## Future Updates

More optimization features and workflow improvements are planned.

---

## License

This project is licensed under the MIT License.

---

## Author

Created by **Kuzey Kayra Eyioğlu**

---

## Connect With Me

<p align="center">
  <a href="https://github.com/KuzeyKayraEyioglu">
    <img src="https://skillicons.dev/icons?i=github" width="90"/>
  </a>
  
  <a href="https://www.youtube.com/@KuzeyKayraEyio%C4%9Flu">
    <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" width="90"/>
  </a>
</p>

<p align="center">
  <a href="https://github.com/KuzeyKayraEyioglu">GitHub</a>
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://www.youtube.com/@KuzeyKayraEyio%C4%9Flu">YouTube</a>
</p>
