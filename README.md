# Computer Vision Technologies — Lab Works Collection

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-arrays-013243)](https://numpy.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-graphics.py-lightgrey)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Collection of lab works for the "Computer Vision Technologies" course (Data Science certificate program with Sigma Software; Igor Sikorsky Kyiv Polytechnic Institute, 2026/2027).

Every lab is stored in its own folder with the source code, the figures it produces, and a detailed README. Labs are written in Python and do not depend on each other.

## Labs

| # | Lab | Description | Source |
|---|---|---|---|
| 1 | **Formation and transformation of 2D and 3D object coordinates** | Matrix geometric transformations in homogeneous coordinates: rotation and translation of a 2D rectangle, composite transformations, and (in progress) a 3D pyramid with axonometric projection and animation | [lab1_coord_technologies_2d_3d/](lab1_coord_technologies_2d_3d/) |

New labs are added to this table as they are completed.

## Technologies

- **Python 3**
- **NumPy** — matrices of vertices and transformation matrices
- **graphics.py** (a wrapper around **Tkinter**) — windows and drawing of polygons
- **OpenCV** — planned for the later labs (feature detection and matching)

## Repository Structure

```text
computer-vision-technologies-labs/
├── README.md
└── lab1_coord_technologies_2d_3d/     # Lab 1 — 2D and 3D coordinate transformations
    ├── main.py
    ├── graphics.py                    # third-party drawing library (see the lab README)
    ├── img/                           # screenshots of the results
    ├── requirements.txt
    └── README.md
```

Each lab is self-contained: it has its own script, figures, and README, so labs can be run or deleted independently.

## How to Run

```bash
git clone https://github.com/<your-username>/computer-vision-technologies-labs.git
cd computer-vision-technologies-labs/lab1_coord_technologies_2d_3d

python -m venv .venv
# Windows:  .venv\Scripts\activate
# Linux/macOS:  source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

Every lab folder has its own `requirements.txt` and its own run instructions in its README.

## How to Add a New Lab

1. Create a folder named `lab<number>_<topic>/` (for example `lab2_...`) with the script, a `requirements.txt` if new packages are needed, and an `img/` folder for results.
2. Add a short `README.md` to the lab folder.
3. Add a new row to the table above and update the repository structure.
4. Commit and push.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The file `graphics.py` is a third-party library by John Zelle released under the GPL; it is kept unchanged with its original header.

---

**Author:** Mariia Stepanova  
**Program:** Software Engineering  
**Institution:** Igor Sikorsky Kyiv Polytechnic Institute (Kyiv, Ukraine)  
**Year:** 2026
