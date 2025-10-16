# app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os, re
from typing import List, Dict

# -------------------- File Picker --------------------
def tk_select_files(multiple=True, filetypes=[("XVG files", "*.xvg")]) -> List[str]:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    if multiple:
        paths = filedialog.askopenfilenames(title="Select all .xvg files", filetypes=filetypes)
    else:
        p = filedialog.askopenfilename(title="Select .xvg file", filetypes=filetypes)
        paths = [p] if p else []
    root.destroy()
    return list(paths)

def tk_select_folder() -> str:
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes("-topmost", 1)
    folder = filedialog.askdirectory(title="Select output folder")
    root.destroy()
    return folder

# -------------------- Property Definitions --------------------
PROPERTIES = {
    "area": {"label": "SASA (Area)", "unit": " (Å²)", "is_rmsf": False, "is_area": True},
    "gyrate": {"label": "Radius of Gyration", "unit": " (Å)", "is_rmsf": False, "is_area": False},
    "hydrogen-bonds": {"label": "Hydrogen Bonds", "unit": " (count)", "is_rmsf": False, "is_area": False},
    "pressure": {"label": "Pressure", "unit": " (bar)", "is_rmsf": False, "is_area": False},
    "rmsd": {"label": "RMSD", "unit": " (Å)", "is_rmsf": False, "is_area": False},
    "rmsf": {"label": "RMSF", "unit": " (Å)", "is_rmsf": True, "is_area": False},
    "temperature": {"label": "Temperature", "unit": " (K)", "is_rmsf": False, "is_area": False},
}

# -------------------- Utility Functions --------------------
def detect_prop(fname):
    name = os.path.basename(fname).lower()
    for k in PROPERTIES.keys():
        if k in name:
            return k
    return ""

def extract_mutant_name(fname):
    base = os.path.splitext(os.path.basename(fname))[0]
    parts = base.split("_")
    return parts[-1] if len(parts) > 1 else base

def load_xvg(path):
    data = []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if line.startswith(("#", "@")):
                continue
            p = line.strip().split()
            if len(p) >= 2:
                try:
                    data.append([float(p[0]), float(p[1])])
                except ValueError:
                    pass
    return np.array(data) if data else np.empty((0, 2))

def convert_units(a, prop):
    out = a.copy()
    if out.size == 0:
        return out
    if not PROPERTIES[prop]["is_rmsf"] and out[-1, 0] > 500:
        out[:, 0] /= 1000.0  # ps → ns
    if PROPERTIES[prop]["is_area"]:
        out[:, 1] *= 100.0
    elif PROPERTIES[prop]["unit"].startswith(" (Å)"):
        out[:, 1] *= 10.0
    return out

def y_limits(arrs, frac=0.1, min_pad=0.05):
    y_all = np.concatenate(arrs) if arrs else np.array([0, 1])
    ymin, ymax = np.nanmin(y_all), np.nanmax(y_all)
    if np.isclose(ymin, ymax):
        pad = max(abs(ymax) * frac, min_pad)
        return ymin - pad, ymax + pad
    span = ymax - ymin
    pad = max(span * frac, min_pad)
    return ymin - pad, ymax + pad

# -------------------- Streamlit UI --------------------
st.set_page_config(page_title="XVG Analyzer", page_icon="📈", layout="wide")
st.title("📈 XVG Analyzer — WT vs Multiple Mutants (Auto-Detect Mode)")
st.caption("Auto-detects RMSD, RMSF, SASA, RoG, Pressure, Temperature, etc. and compares WT vs all mutants.")

st.markdown("### 1️⃣ Select Input Files and Output Folder")

col1, col2 = st.columns(2)
with col1:
    if st.button("📂 Select All XVG Files"):
        sel = tk_select_files(multiple=True)
        if sel:
            st.session_state["files"] = sel
    files = st.session_state.get("files", [])
    st.write(f"**{len(files)} files selected.**" if files else "_No files selected_")

with col2:
    if st.button("💾 Choose Save Folder"):
        folder = tk_select_folder()
        if folder:
            st.session_state["out"] = folder
    out_dir = st.session_state.get("out", "")
    st.write("**Save to:**", out_dir if out_dir else "_Not selected_")

st.markdown("---")

# Detect all mutants for color selection
mutant_names = []
if files:
    for f in files:
        if "_" in os.path.basename(f).split('.')[0]:
            mname = extract_mutant_name(f)
            if mname not in mutant_names:
                mutant_names.append(mname)
mutant_names = sorted(mutant_names)

st.markdown("### 2️⃣ Plot Appearance")
colA, colB = st.columns(2)
wt_color = colA.color_picker("WT Color", "#000000")
grid = st.checkbox("Show Grid", True)
legend_loc = st.selectbox("Legend Position",
                          ["best", "upper right", "upper left", "lower right", "lower left"], index=0)

mutant_colors = {}
if mutant_names:
    st.markdown("#### 🎨 Mutant Colors")
    for m in mutant_names:
        mutant_colors[m] = st.color_picker(f"Color for {m}", "#E41A1C")

# -------------------- Main Plot Logic --------------------
if st.button("🚀 Generate All Detected Plots"):
    if not files:
        st.error("Please select .xvg files first.")
        st.stop()
    if not out_dir or not os.path.exists(out_dir):
        st.error("Please select a valid output folder.")
        st.stop()

    # Group files by property
    grouped = {}
    for f in files:
        key = detect_prop(f)
        if not key:
            continue
        if key not in grouped:
            grouped[key] = {"wt": None, "mutants": []}
        if "_" in os.path.basename(f).split('.')[0]:
            grouped[key]["mutants"].append(f)
        else:
            grouped[key]["wt"] = f

    if not grouped:
        st.error("No recognized property files found.")
        st.stop()

    # Auto grid layout
    nplots = len(grouped)
    ncols = 3 if nplots > 4 else 2
    nrows = (nplots + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 5, nrows * 4), dpi=150)
    axes = axes.flatten()

    i = 0
    for prop, entry in grouped.items():
        ax = axes[i]
        i += 1

        wt_file = entry["wt"]
        mutants = entry["mutants"]

        if not wt_file:
            ax.text(0.5, 0.5, f"No WT for {prop}", ha="center", va="center", fontsize=10)
            continue
        if not mutants:
            ax.text(0.5, 0.5, f"No mutants for {prop}", ha="center", va="center", fontsize=10)
            continue

        wt = convert_units(load_xvg(wt_file), prop)
        mut_arrays = [(extract_mutant_name(m), convert_units(load_xvg(m), prop)) for m in mutants if os.path.exists(m)]

        if wt.size == 0:
            ax.text(0.5, 0.5, f"Empty data: {prop}", ha="center", va="center", fontsize=10)
            continue

        # WT plot
        ax.plot(wt[:, 0], wt[:, 1], color=wt_color, linewidth=1.8, label="WT")

        # Mutants (individual colors)
        for name, arr in mut_arrays:
            color = mutant_colors.get(name, "#1f77b4")
            if arr.size == 0:
                continue
            ax.plot(arr[:, 0], arr[:, 1], linestyle="--", linewidth=1.3, color=color, label=name)

        # Format axes
        ax.set_xlabel("Residue Index" if PROPERTIES[prop]["is_rmsf"] else "Time (ns)")
        ax.set_ylabel(PROPERTIES[prop]["label"] + PROPERTIES[prop]["unit"])
        ax.set_title(PROPERTIES[prop]["label"])
        ax.legend(loc=legend_loc, frameon=True)
        ax.set_xlim(left=0)
        ax.margins(x=0)
        ylo, yhi = y_limits([wt[:, 1]] + [a[:, 1] for _, a in mut_arrays])
        ax.set_ylim(ylo, yhi)
        if grid:
            ax.grid(True, linestyle="--", alpha=0.5)

        # Save PNG
        out_path = os.path.join(out_dir, f"{prop}_comparison.png")
        fig_single, ax_single = plt.subplots(figsize=(8, 6), dpi=150)
        ax_single.plot(wt[:, 0], wt[:, 1], color=wt_color, linewidth=1.8, label="WT")
        for name, arr in mut_arrays:
            color = mutant_colors.get(name, "#1f77b4")
            ax_single.plot(arr[:, 0], arr[:, 1], linestyle="--", linewidth=1.3, color=color, label=name)
        ax_single.set_xlabel("Residue Index" if PROPERTIES[prop]["is_rmsf"] else "Time (ns)")
        ax_single.set_ylabel(PROPERTIES[prop]["label"] + PROPERTIES[prop]["unit"])
        ax_single.set_title(f"{PROPERTIES[prop]['label']} — WT vs Mutants")
        ax_single.legend(loc=legend_loc)
        ax_single.set_xlim(left=0)
        ax_single.margins(x=0)
        if grid:
            ax_single.grid(True, linestyle="--", alpha=0.5)
        fig_single.tight_layout()
        fig_single.savefig(out_path, dpi=300, bbox_inches="tight")
        plt.close(fig_single)

    for j in range(i, len(axes)):
        axes[j].axis("off")

    fig.tight_layout()
    st.pyplot(fig)
    st.success(f"✅ {i} plots generated and saved in: {out_dir}")

st.markdown(
    """
    <hr/>
    <small>
    • WT solid line, mutants dashed.<br>
    • Each mutant has its own selectable color.<br>
    • X-axis starts at 0, no gaps.<br>
    • All detected properties displayed and saved automatically.<br>
    </small>
    """,
    unsafe_allow_html=True
)
