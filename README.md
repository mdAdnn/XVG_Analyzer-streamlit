# 📈 XVG Analyzer — WT vs Multiple Mutants (Auto-Detect Mode)

A lightweight **Streamlit app** for automated visualization and analysis of GROMACS `.xvg` output files.  
Easily compare **wild type (WT)** and **multiple mutants** across key structural and thermodynamic properties — all in a single run!

---

## 🚀 Features

✅ Auto-detects common GROMACS outputs:
- RMSD  
- RMSF  
- SASA (Surface Area)  
- Radius of Gyration (RoG)  
- Pressure  
- Temperature  
- Hydrogen Bonds  

✅ Detects WT vs. all mutant files automatically  
✅ Individual color pickers for each mutant  
✅ Combined grid plots + separate PNGs for each property  
✅ Auto unit conversion (ps → ns, Å², etc.)  
✅ Simple file & folder picker (native dialog)  
✅ Cross-platform (Windows, macOS, Linux)

---

## 🧩 Quick Workflow

1️⃣ Select all `.xvg` files (WT + mutants)  
2️⃣ Choose an output folder  
3️⃣ Customize colors per mutant  
4️⃣ Click **“🚀 Generate All Detected Plots”**

✅ The app auto-detects and plots all properties  
✅ High-resolution PNGs are saved automatically

---

## 📁 Directory Structure

D:
└── XVG_Analyzer-streamlit
├── app.py ← Main Streamlit app
├── requirements.txt ← Dependencies
├── venv\ ← Virtual environment
│ ├── Scripts
│ └── Lib
├── logo.ico ← Optional app icon
├── LICENSE ← License file (optional)
├── README.md ← This file!
└── (Output PNGs saved to folder you select inside the app)


---

## 🧠 Requirements

- Python **3.9 – 3.12**  
  (⚠️ Python 3.13 is still experimental for Streamlit)
- Tkinter (included by default on Windows/macOS)

If using **Linux**, install Tkinter manually:
```bash
sudo apt install python3-tk

⚙️ Installation
1️⃣ Clone or download this repository
git clone https://github.com/<your-username>/XVG_Analyzer-streamlit.git
cd XVG_Analyzer-streamlit

2️⃣ Create and activate a virtual environment

Windows (PowerShell):

python -m venv venv
.\venv\Scripts\activate


macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

▶️ Run the App

Start the Streamlit app:

streamlit run app.py


Streamlit will show something like:

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501


If it doesn’t open automatically, visit:
👉 http://localhost:8501

🧪 Example Usage

1️⃣ Select All XVG Files
Select all .xvg files (e.g., rmsd.xvg, rmsd_T645M.xvg, rmsd_V698I.xvg).

2️⃣ Choose Output Folder
Pick where you want to save the generated PNGs.

3️⃣ Customize Colors
Each mutant has its own color picker.

4️⃣ Generate Plots
Click 🚀 Generate All Detected Plots

✅ The app will:

Display all plots in a clean grid (2×2 or 3×3 layout)

Save each property plot as a high-resolution PNG

📊 Output Examples

Each detected property produces:

A combined comparison plot (WT + all mutants)

A saved PNG named like:

rmsd_comparison.png
rmsf_comparison.png
area_comparison.png

🧰 One-Click Launch Options
🪟 Windows — with virtual environment

Create a file named run_app.bat:

@echo off
call venv\Scripts\activate
streamlit run app.py
pause


Then just double-click it.

🪟 Windows — without virtual environment

If users don’t want to create venv, use this instead:

@echo off
python -m streamlit run app.py
pause


(Requires Streamlit installed globally: pip install streamlit numpy matplotlib)

🍎🐧 macOS / Linux

Create a script run_app.sh:

#!/bin/bash
source venv/bin/activate
streamlit run app.py


Make it executable:

chmod +x run_app.sh


Or, for global Python:

#!/bin/bash
python3 -m streamlit run app.py

⚡ Universal Launcher (Optional)

To make the tool fully plug-and-play across OSes, include this simple launcher:

launch.py

import subprocess, sys
try:
    import streamlit
except ImportError:
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit", "numpy", "matplotlib"])
subprocess.run(["streamlit", "run", "app.py"])


Then users can just run:

python launch.py


✅ Works on Windows, macOS, and Linux
✅ Automatically installs dependencies if missing

🧪 Tested Environment
Component	Version
Windows	11
Python	3.10 / 3.11
Streamlit	1.39+
Matplotlib	3.8+
NumPy	1.26+
🧠 Notes

WT = solid line, mutants = dashed lines

Time automatically converted from ps → ns

Mutant colors stay consistent across properties

Unicode units (Å, Å²) supported

Clean adaptive layout (2×2 / 3×3 grid)

📜 License

This project is licensed under the MIT License — see the LICENSE
 file for details.

💡 Citation / Acknowledgment

If this app contributes to your research, please cite:

Adnan, M. (2025). XVG Analyzer — Streamlit-based visualization tool for GROMACS trajectories.