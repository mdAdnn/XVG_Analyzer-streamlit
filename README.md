# 🧬 XVG Analyzer

A simple, offline Streamlit app to compare GROMACS `.xvg` outputs (RMSD, RMSF, Radius of Gyration, SASA) between wildtype and mutant simulations.

---

## 🔧 Features
- Select one **WT** and multiple **mutant** `.xvg` files  
- Choose **output folder** for saving plots  
- Auto-unit conversion:
  - Time → ns
  - RMSD/RMSF/RoG → Å
  - SASA → Å²
- Saves publication-ready 300dpi PNGs  
- Download ZIP with all generated plots  
- Works **offline** — perfect for labs and classrooms

---

## 🧠 Run Locally
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
