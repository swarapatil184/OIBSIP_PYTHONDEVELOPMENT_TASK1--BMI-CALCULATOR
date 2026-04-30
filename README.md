# ⚖ BMI Calculator Pro

A feature-rich desktop BMI tracking application built with Python and Tkinter, featuring a dark-themed UI, persistent user history, and optional trend charts.

---

## Features

- **BMI Calculator** — Compute BMI from weight (kg) and height (cm) with instant category classification
- **Visual Gauge** — Color-coded gauge bar showing where your BMI falls across all categories
- **User Profiles** — Save and manage multiple users with full measurement history
- **History Tab** — View past records in a sortable table; delete users when needed
- **Trend Graph** — Optional matplotlib chart showing your BMI trend over time
- **BMI Guide** — Built-in reference tab covering all WHO BMI categories with health tips

---

## Requirements

- Python 3.7+
- `tkinter` (included with standard Python on Windows/macOS; on Linux: `sudo apt install python3-tk`)
- `matplotlib` *(optional — required only for the Trend Graph feature)*

Install the optional dependency:

```bash
pip install matplotlib
```

---

## Getting Started

```bash
# Clone or download the project
git clone https://github.com/your-username/bmi-calculator-pro.git
cd bmi-calculator-pro

# Run the app
python bmi_calculator.py
```

No additional setup required. The app creates a `bmi_data.json` file in the same directory to persist user data.

---

## Usage

### Calculator Tab
1. Enter a **Name / User ID** (used to associate your records).
2. Enter your **Weight** in kilograms (20–300 kg).
3. Enter your **Height** in centimetres (50–250 cm).
4. Click **Calculate BMI** — your result, category, and a health tip will appear instantly.
5. Each calculation is automatically saved.

### History Tab
- Select a user from the dropdown and click **Load** to view their records.
- Click **📈 Trend Graph** to visualize BMI change over time (requires matplotlib and at least 2 records).
- Click **Delete User** to permanently remove a user and all their data.

### BMI Guide Tab
A quick reference for all BMI categories, color-coded by risk level, along with the BMI formula and a disclaimer note.

---

## BMI Categories

| Category | BMI Range | Color |
|---|---|---|
| Underweight | < 18.5 | 🔵 Blue |
| Normal weight | 18.5 – 24.9 | 🟢 Green |
| Overweight | 25.0 – 29.9 | 🟡 Orange |
| Obese (Class I) | 30.0 – 34.9 | 🟠 Dark Orange |
| Obese (Class II) | 35.0 – 39.9 | 🔴 Red |
| Obese (Class III) | ≥ 40.0 | 🔴 Dark Red |

---

## Data Storage

User data is saved locally to `bmi_data.json` in the application directory. No data is sent to any server.

**File format example:**
```json
{
  "Alice": [
    {
      "date": "2025-04-30 10:42",
      "weight": 65.0,
      "height": 168.0,
      "bmi": 23.03,
      "category": "Normal weight"
    }
  ]
}
```

---

## Project Structure

```
bmi-calculator-pro/
├── bmi_calculator.py   # Main application
├── bmi_data.json       # Auto-generated user data file
└── README.md
```

---

## Disclaimer

BMI is a screening tool, not a diagnostic measure. Consult a qualified healthcare professional for a complete health assessment.

---

## License

MIT License — free to use, modify, and distribute.
