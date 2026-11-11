# Lab 1 — Formation and transformation of 2D and 3D object coordinates

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-arrays-013243)](https://numpy.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-graphics.py-lightgrey)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python script that builds geometric figures from a matrix of vertices and transforms them with matrix operations in homogeneous coordinates. Developed as the first lab work for the "Computer Vision Technologies" course (Igor Sikorsky Kyiv Polytechnic Institute, 2026/2027). Assignment variant: **17**.

The script draws the figures with `graphics.py` (a wrapper around Tkinter) and does all the calculations with `NumPy`. The window size, the size of the figures, the animation parameters, and the colours are chosen freely, as the assignment allows.

Back to the [list of all labs](../README.md).

## Assignment (Variant 17)

| Level | Figure | Requirements | Max points | Status |
|---|---|---|---|---|
| I (2D) | Rectangle | Operations: rotation, then (rotation + translation). The second operation is cyclic, the trajectory is hidden. All transformations stay inside the window. The input matrix of corners is extended. Matrix operations and composite transformations | 8 | Done |
| II (3D) | Pyramid with a triangular base | Axonometric projection, cyclic rotation around an internal axis, the trajectory is hidden. Dynamics: the figure appears and fades, appears in different parts of the window, changes the fill colour | 9 | Done |
| III | Both | Level I and level II in one script | 10 | Done |

## Mathematical Model

### Homogeneous coordinates

A point `(x, y)` is written as `(x, y, 1)`. The extra `1` lets translation be written as a matrix multiplication, like rotation and scaling, so any chain of transformations can be multiplied into one matrix.

The figure is stored as a table where **each row is a vertex**:

```text
rect = | x1  y1  1 |
       | x2  y2  1 |
       | x3  y3  1 |
       | x4  y4  1 |
```

### Transformation matrices (2D)

```text
Translation T(dx, dy)        Rotation R(a)
| 1  0  dx |                 | cos a  -sin a  0 |
| 0  1  dy |                 | sin a   cos a  0 |
| 0  0  1  |                 | 0       0      1 |
```

On the screen the Y axis points down, so a positive angle looks like a clockwise rotation.

### Rows instead of columns

The matrices above are written for a vertex stored as a column. Because the vertices are stored as rows, the transformation is applied as

```text
new_figure = figure · Mᵀ
```

This gives the same coordinates as `M · p` for a column vertex.

### Composite transformation

Rotation around the centre `c = (cx, cy)` of the figure:

```text
M = T(cx, cy) · R(a) · T(-cx, -cy)
```

Read right to left: move the centre to the origin, rotate, move back. Rotation together with translation along the X axis:

```text
M = T(shift, 0) · T(cx, cy) · R(a) · T(-cx, -cy)
```

The matrix is always applied to the **original** figure, not to the previous frame, so rounding errors do not accumulate.

### Staying inside the window

A rectangle of size `w × h` at any angle fits into a circle with the radius of its half-diagonal `r = sqrt(w² + h²) / 2`. The centre is not allowed to come closer than `r` (plus a margin) to the window edge, so the vertices never leave the window.

### 3D model (level II)

Four-dimensional homogeneous coordinates `(x, y, z, 1)` and 4×4 matrices: translation `T`, rotations `Rx` and `Ry`, and an orthographic projection onto the XY plane (`diag(1, 1, 0, 1)`).

**Pyramid.** The base is a regular triangle of radius `r = 60` with vertices at 90°, 210° and 330°, the apex is above it, the height is `h = 140`. The centre `(cx, cy, cz)` is the centre of mass of the four vertices: the base lies `h/4` below the centre and the apex `3h/4` above it, so the pyramid rotates around its own axis.

**Isometric projection.** Rotation around Y by 45°, then around X by 35.264° (`arcsin(tan 30°)`), then the `z` coordinate is dropped. On the screen the Y axis points down, so the tilt has the minus sign. The cyclic rotation around the own axis adds the angle `spin` to the 45°:

```text
M_view = T(c) · Rx(-35.264°) · Ry(45° + spin) · T(-c)
frame  = V · M_viewᵀ
flat   = frame · Pᵀ
```

**Faces.** The four faces are filled and drawn with the painter's algorithm: the Z axis points to the viewer, the faces are sorted by the mean `z` of their vertices and drawn from the farthest to the nearest. Hidden edges are not drawn, the model is opaque.

**Dynamics.** One appearance lasts 120 frames. The visibility `t = min(1, k/20, (120-k)/20)` grows during the first 20 frames, stays at 1, and falls during the last 20 frames. `graphics.py` has no transparency, so the colour is blended with the white background: `c' = 255 - (255 - c)·t`. Each appearance picks a random centre (`cx` in 110..590, `cy` in 110..390, so the pyramid always stays in the window) and a random base colour. The faces have different brightness (0.6, 0.8, 1.0, 0.7).

## Level I — How the Script Works

1. Open the window and build the extended 4×3 matrix of rectangle corners around the window centre.
2. **Operation 1:** for the angle from 0° to 355° with a step of 5°, build `T(c) · R(angle) · T(-c)`, apply it to the original rectangle, erase the previous frame, draw the new one.
3. **Operation 2:** in a loop until a mouse click, change the angle by 5° and the shift by 4 px, bounce the shift back at the limit, build `T(shift) · T(c) · R(angle) · T(-c)`, erase the previous frame, draw the new one.
4. Because the previous frame is erased before each new one, the trajectory is not displayed.
5. A mouse click ends the loop and closes the window.

The mouse position over the window is shown at the top, which helps to check vertex coordinates by hand.

## Level II — How the Script Works

1. Pick a random centre and a random base colour, build the 4×4 matrix of the pyramid vertices.
2. For each of the 120 frames build `M_view`, apply it to the original vertices, project them onto the XY plane and sort the faces by depth.
3. Draw the filled faces with the faded colour, show the frame with `win.update()`, erase the frame.
4. After 120 frames the pyramid has made one full turn and has faded out; the next appearance starts at another place with another colour. A mouse click ends the loop.

## Level III

`main.py` opens one window, runs `task_2d` (level I) until a mouse click, then `task_3d` from `pyramid.py` (level II) until the next click.

## Folder Structure

```text
lab1_coord_technologies_2d_3d/
├── main.py                          # entry point and level I (2D)
├── pyramid.py                       # level II (3D)
├── graphics.py                      # drawing library by John Zelle (GPL), unchanged
├── img/                             # screenshots of the results
├── requirements.txt                 # Python dependencies
└── README.md
```

## How to Run

1. Install Python 3 (with Tkinter; on Linux: `sudo apt install python3-tk`) and create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   # Windows:  .venv\Scripts\activate
   # Linux/macOS:  source .venv/bin/activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   `graphics.py` is not installed with pip: it is a single file that must lie next to `main.py`.

3. Run the script from this folder:

   ```bash
   python main.py
   ```

First the blue rectangle makes a full turn around its centre. Then the orange rectangle rotates and moves left and right until a mouse click. After the click the pyramid appears, rotates, fades and appears again at another place with another colour; the next click closes the window. Do not close the window with the cross during the animation, otherwise Tkinter prints an error.

## Results

| Operation 1: rotation around the centre              | Operation 2: rotation + translation                |
|------------------------------------------------------|----------------------------------------------------|
| ![Rotation and translation](img/level1_rotation.gif) | ![Rotation and translation](img/level1_motion.gif) |

## Verification

- The step-by-step result (`T(-c)`, then `R`, then `T(c)`) matches the result of the single composite matrix (`np.allclose` returns `True`).
- The matrix result for a vertex matches the scalar formulas `x' = cx + (x - cx)·cos a - (y - cy)·sin a`, `y' = cy + (x - cx)·sin a + (y - cy)·cos a`.
- Over the whole animation the vertices stay inside the window: `x` from 9.6 to 690.4 (window width 700), `y` from 158 to 342 (window height 500).
- The vertex coordinates printed in the console match the coordinates shown by the mouse position label.
- 3D: the mean `y` of the vertices is 250 and the height is 140, so the centre is the centre of mass; the projected unit vectors of all three axes have the same length 0.8165, so the projection is isometric.
- 3D: for the extreme positions of the centre and all rotation angles the vertices stay inside the window (`x` from 50 to 650, `y` from 24.3 to 453.2).
- A full run (level I, level II, exit by click) works without errors.

## The Process

- Analysis of the assignment and of the lecture material on 2D and 3D geometric transformations
- Choice of the model: homogeneous coordinates, composition of matrices, vertices stored as rows
- Hand calculation of the corners and of the first frames, checking them against the console and the mouse position
- Implementation of the transformation matrices and the animation loop
- Fixing animation bugs (leftover frames, wrong rotation direction, a fixed angle inside the loop)
- Writing the report with the model, the architecture, the code, the screenshots, and the conclusions

## What I Learned

- Why a point gets an extra `1`: it turns translation into a matrix product
- How a matrix is multiplied (row times column) and why it is transposed when the vertices are stored as rows
- Why the order of matrices matters: `T(c) · R · T(-c)` rotates around the centre, other orders do not
- That a skipped transpose in rotation does not crash the program: the figure just rotates the other way, so results must be checked by numbers
- That the Y axis on the screen points down, so a positive angle is clockwise
- How the animation works: calculate the frame, erase the previous one, draw the new one, wait
- How to keep a rotating figure inside the window using the half-diagonal
- How the isometric projection is built from two rotations and the dropped `z` coordinate
- Why the painter's algorithm needs faces sorted by depth
- Why `graphics.py` flickers with the default autoflush and how `autoflush=False` with one `win.update()` per frame fixes it

## How It Could Be Improved

- Add scaling and the `T · R · S` chain
- Add motion along both axes with bouncing off all four edges
- Replace the orthographic projection with a perspective projection
- Add a perspective projection and a lighting model for the faces
- Move the matrix functions to a separate module and add tests for the key values (for example, `R(90°)` maps `(1, 0)` to `(0, 1)`)
- Add sliders to change the angle step and the speed

---

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

The file `graphics.py` is a third-party library by John Zelle released under the GPL; it is kept unchanged with its original header.

---

**Author:** Mariia Stepanova  
**Program:** Software Engineering  
**Institution:** Igor Sikorsky Kyiv Polytechnic Institute (Kyiv, Ukraine)  
**Year:** 2026
