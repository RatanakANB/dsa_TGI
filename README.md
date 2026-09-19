# RPL Candidate Analytics & Interactive Dashboard

An end-to-end Data Analytics project for exploring candidate recognition of prior learning (RPL) data. This project includes both an interactive **Streamlit Web Application** (`app.py`) and pre-executed **Jupyter Notebooks** (`assessment.ipynb` / `assestment.ipynb`).

---

## 📁 Repository Structure

```text
assignment/
├── RPL_Dashboard_V.1.csv    # Raw RPL Candidate Dataset
├── app.py                   # Streamlit Interactive Dashboard Application (Cross-Platform)
├── assessment.ipynb         # Jupyter Notebook (Dual DataFrame: df_kh & df_en)
├── assestment.ipynb         # Jupyter Notebook (Identical Copy)
├── requirements.txt         # Python Package Dependencies
└── README.md                # Project Setup & User Guide
```

---

## 🌐 Cross-Platform Compatibility

`app.py` is designed to run seamlessly out-of-the-box on **Windows**, **macOS**, **Linux**, **Docker**, and **Streamlit Community Cloud** without OS-specific hardcoded paths.

---

## 🚀 Quick Start & Installation Guide

Follow these steps to set up the environment and run the project out-of-the-box.

### 1. Clone / Open Project Folder
Open your terminal or VS Code command prompt in the project directory:
```bash
cd assignment
```

### 2. Create & Activate Virtual Environment (Recommended)

**On Windows (PowerShell / CMD):**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
Install all required Python packages with a single command:
```bash
pip install -r requirements.txt
```

---

## 📊 1. How to Run the Streamlit Interactive Dashboard

Launch the Streamlit Web Application locally:
```bash
streamlit run app.py
```
*(Alternative command if `streamlit` is not in your global PATH: `python -m streamlit run app.py`)*

Once started, the dashboard will open automatically in your browser at:  
👉 **http://localhost:8501**

### Dashboard Features:
- **Interactive Sidebar Date Filters** dynamically fetched from `Date_Committee_Meeting`:
  - **1. Specific Meeting Date (`[Committee_Meeting(date)]`)**: Easy multiselect dropdown for the 13 exact committee meeting dates (`11/16/2020`, `11/30/2021`, `12/4/2021`, `12/19/2021`, `1/26/2022`, `4/29/2022`, `5/7/2022`, `5/20/2022`, `5/26/2022`, `8/26/2022`, `9/23/2022`, `2/22/2023`, `6/5/2023`).
  - **2. Committee Meeting Year (`[Committee_Meeting(year)]`)**: Multiselect filter for `2020`, `2021`, `2022`, `2023`.
  - **3. Committee Meeting Quarter (`[Committee_Meeting(Quarter)]`)**: Multiselect filter for `Qtr1`, `Qtr2`, `Qtr3`, `Qtr4`.
  - **4. Committee Meeting Month (`[Committee_Meeting(Month)]`)**: Multiselect filter for `Jan` through `Dec`.
- **5 Key Findings (Tabs with Khmer Tables & Interactive Plotly Charts)**:
  1. **Gender Distribution (`Gender_KH`)**: Donut chart (black percentage text) + Summary Table (`ប្រុស`, `ស្រី`, `Total`).
  2. **Occupation (`Occupation_KH`)**: Stacked horizontal bar chart + Summary Table (`ប្រុស`, `ស្រី`, `Total`).
  3. **Assessment Center (`AT_KH`)**: Stacked horizontal bar chart + Summary Table (`ប្រុស`, `ស្រី`, `Total`).
  4. **Qualification Level (`NQ_KH`)**: Grouped bar chart + Summary Table (`ប្រុស`, `ស្រី`, `Total`).
  5. **Sponsor (`Sponsors`)**: Stacked bar chart + Summary Table (`ប្រុស`, `ស្រី`, `Total`).

---

## 📓 2. How to Open & Run the Jupyter Notebook in VS Code

No full Jupyter installation is required! You can open and interact with the `.ipynb` notebooks directly in **VS Code**.

### Steps for VS Code:
1. Open **VS Code** and install the **Jupyter Extension** (by Microsoft):
   - Open Extensions (`Ctrl+Shift+X` or `Cmd+Shift+X`).
   - Search for **Jupyter** (`ms-toolsai.jupyter`) and click **Install**.
2. Open [assessment.ipynb](file:///d:/08.SCHOOL/TGI-DSA/assignment/assessment.ipynb) or [assestment.ipynb](file:///d:/08.SCHOOL/TGI-DSA/assignment/assestment.ipynb).
3. In the top-right corner of the notebook editor, click **Select Kernel** and choose your Python environment (`venv` or `Python 3.x`).
4. Click **Run All** or execute cells individually using `Shift + Enter`.

### Notebook Highlights:
- **Dual DataFrame Architecture**:
  - `df_kh`: Khmer DataFrame containing `Occupation_KH`, `NQ_KH`, `AT_KH`, `Gender_KH` for internal analysis & exploration.
  - `df_en`: English DataFrame containing `Occupation_EN`, `NQ_EN`, `AT_EN`, `Gender_EN` for visualization plots and English tables.
- **Clean Schema**: All `Serial_Code`, `Path`, `Pics`, `CardNo`, `DI_*`, and `DE_*` columns are dropped.

---

## 🧹 Dataset Cleaning & Filtering Summary

| Action | Columns Affected |
| :--- | :--- |
| **Dropped Explicit Columns** | `Serial_Code`, `Path`, `Pics`, `CardNo` |
| **Dropped Issue Date Columns** | `Date_Issue_EN`, `DI_Day_KH`, `DI_Month_KH`, `DI_Year_KH` |
| **Dropped Expiry Date Columns** | `Date_Expiry_EN`, `DE_Day_KH`, `DE_Month_KH`, `DE Year (KH)` |
| **Parsed for Filters** | `Date_Committee_Meeting` -> 13 Meeting Dates, Year, Quarter (`Qtr1`-`Qtr4`), Month (`Jan`-`Dec`) |
| **Analyzed Attributes** | `Gender_KH`, `Occupation_KH`, `AT_KH`, `NQ_KH`, `Sponsors` |

---

## 🛠️ Troubleshooting & Notes

- **Font Support for Khmer Text**: Matplotlib charts in the notebook configure system Khmer fonts. Plotly charts in Streamlit render UTF-8 Khmer text natively in your browser on all OS platforms.
- **Port Conflict**: If port `8501` is in use when starting Streamlit, pass `--server.port 8502` to use an alternative port.
