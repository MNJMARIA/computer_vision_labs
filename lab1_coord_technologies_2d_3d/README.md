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
| II (3D) | Pyramid with a triangular base | Axonometric projection, cyclic rotation around an internal axis, the trajectory is hidden. Dynamics: the figure appears and fades, appears in different parts of the window, changes the fill colour | 9 | In progress |
| III | Both | Level I and level II in one script | 10 | In progress |

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

### 3D model (level II, in progress)

Four-dimensional homogeneous coordinates `(x, y, z, 1)`, 4×4 matrices, rotation around the pyramid's own vertical axis, isometric projection (rotation around Y by 45° and around X by 35.264°, then dropping `z`), and painter's-algorithm ordering of the faces. This section is updated when level II is finished.

## Level I — How the Script Works

1. Open the window and build the extended 4×3 matrix of rectangle corners around the window centre.
2. **Operation 1:** for the angle from 0° to 355° with a step of 5°, build `T(c) · R(angle) · T(-c)`, apply it to the original rectangle, erase the previous frame, draw the new one.
3. **Operation 2:** in a loop until a mouse click, change the angle by 5° and the shift by 4 px, bounce the shift back at the limit, build `T(shift) · T(c) · R(angle) · T(-c)`, erase the previous frame, draw the new one.
4. Because the previous frame is erased before each new one, the trajectory is not displayed.
5. A mouse click ends the loop and closes the window.

The mouse position over the window is shown at the top, which helps to check vertex coordinates by hand.

## Folder Structure

```text
lab1_coord_technologies_2d_3d/
├── main.py                          # Level I (2D) and level II (3D)
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

First the blue rectangle makes a full turn around its centre. Then the orange rectangle rotates and moves left and right until a mouse click closes the window. Do not close the window with the cross during the animation, otherwise Tkinter prints an error.

## Results

| Operation 1: rotation around the centre              | Operation 2: rotation + translation                |
|------------------------------------------------------|----------------------------------------------------|
| ![Rotation and translation](img/level1_rotation.gif) | ![Rotation and translation](img/level1_motion.gif) |

## Verification

- The step-by-step result (`T(-c)`, then `R`, then `T(c)`) matches the result of the single composite matrix (`np.allclose` returns `True`).
- The matrix result for a vertex matches the scalar formulas `x' = cx + (x - cx)·cos a - (y - cy)·sin a`, `y' = cy + (x - cx)·sin a + (y - cy)·cos a`.
- Over the whole animation the vertices stay inside the window: `x` from 9.6 to 690.4 (window width 700), `y` from 158 to 342 (window height 500).
- The vertex coordinates printed in the console match the coordinates shown by the mouse position label.

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

## How It Could Be Improved

- Add scaling and the `T · R · S` chain
- Add motion along both axes with bouncing off all four edges
- Replace the orthographic projection with a perspective projection
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
