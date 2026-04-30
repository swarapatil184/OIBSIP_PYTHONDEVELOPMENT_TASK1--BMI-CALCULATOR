

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
import math


try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# ─── Constants ────────────────────────────────────────────────────────────────
DATA_FILE = "bmi_data.json"

BMI_CATEGORIES = [
    (0,    18.5, "Underweight",      "#3498db"),
    (18.5, 25.0, "Normal weight",    "#2ecc71"),
    (25.0, 30.0, "Overweight",       "#f39c12"),
    (30.0, 35.0, "Obese (Class I)",  "#e67e22"),
    (35.0, 40.0, "Obese (Class II)", "#e74c3c"),
    (40.0, 999,  "Obese (Class III)","#c0392b"),
]

# ─── Helper Functions ──────────────────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI from weight (kg) and height (m)."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return round(weight_kg / (height_m ** 2), 2)


def classify_bmi(bmi: float) -> tuple:
    """Return (category_label, hex_color) for a given BMI."""
    for low, high, label, color in BMI_CATEGORIES:
        if low <= bmi < high:
            return label, color
    return "Unknown", "#95a5a6"


def load_data() -> dict:
    """Load user BMI history from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data: dict) -> None:
    
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def validate_float(value: str, field_name: str, min_val: float, max_val: float) -> float:
    
    try:
        v = float(value)
    except ValueError:
        raise ValueError(f"{field_name} must be a number.")
    if not (min_val <= v <= max_val):
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}.")
    return v


# ─── Main Application ──────────────────────────────────────────────────────────
class BMIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator Pro")
        self.geometry("780x620")
        self.resizable(True, True)
        self.configure(bg="#1a1a2e")

        self.data = load_data()
        self.current_user = tk.StringVar(value="")

        self._build_styles()
        self._build_ui()

    # ── Styles ────────────────────────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TNotebook", background="#1a1a2e", borderwidth=0)
        style.configure("TNotebook.Tab",
                         background="#16213e", foreground="#a0a8c0",
                         padding=[14, 8], font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", "#0f3460")],
                  foreground=[("selected", "#e94560")])

        style.configure("TFrame", background="#1a1a2e")
        style.configure("Card.TFrame", background="#16213e", relief="flat")

        style.configure("TLabel", background="#1a1a2e", foreground="#c8d0e0",
                         font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#1a1a2e", foreground="#e94560",
                         font=("Segoe UI", 18, "bold"))
        style.configure("Result.TLabel", background="#16213e", foreground="#ffffff",
                         font=("Segoe UI", 28, "bold"))
        style.configure("Category.TLabel", background="#16213e",
                         font=("Segoe UI", 13, "bold"))
        style.configure("Card.TLabel", background="#16213e", foreground="#c8d0e0",
                         font=("Segoe UI", 10))

        style.configure("Accent.TButton",
                         background="#e94560", foreground="white",
                         font=("Segoe UI", 11, "bold"), padding=[14, 8],
                         borderwidth=0)
        style.map("Accent.TButton",
                  background=[("active", "#c73652"), ("pressed", "#a52d44")])

        style.configure("TEntry", fieldbackground="#0f3460", foreground="white",
                         insertcolor="white", font=("Segoe UI", 11),
                         borderwidth=0, padding=6)
        style.configure("TCombobox", fieldbackground="#0f3460", foreground="white",
                         background="#0f3460", font=("Segoe UI", 11))

        style.configure("Treeview",
                         background="#0f3460", foreground="#c8d0e0",
                         rowheight=26, fieldbackground="#0f3460",
                         font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                         background="#16213e", foreground="#e94560",
                         font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#e94560")])

    # ── UI Layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#0f3460", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="⚖  BMI Calculator Pro",
                 bg="#0f3460", fg="#e94560",
                 font=("Segoe UI", 20, "bold")).pack(side="left", padx=20)
        tk.Label(header, text="Track · Analyse · Improve",
                 bg="#0f3460", fg="#a0a8c0",
                 font=("Segoe UI", 10)).pack(side="right", padx=20)

        # Notebook tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_calc    = ttk.Frame(self.notebook)
        self.tab_history = ttk.Frame(self.notebook)
        self.tab_info    = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_calc,    text="  Calculator  ")
        self.notebook.add(self.tab_history, text="  History  ")
        self.notebook.add(self.tab_info,    text="  BMI Guide  ")

        self._build_calculator_tab()
        self._build_history_tab()
        self._build_info_tab()

    # ── Calculator Tab ────────────────────────────────────────────────────────
    def _build_calculator_tab(self):
        outer = self.tab_calc
        outer.configure(style="TFrame")

        # Left panel – inputs
        left = tk.Frame(outer, bg="#16213e", padx=20, pady=20)
        left.pack(side="left", fill="y", padx=(10, 5), pady=10)

        tk.Label(left, text="Enter Your Details",
                 bg="#16213e", fg="#e94560",
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=0,
                 columnspan=2, sticky="w", pady=(0, 14))

        fields = [
            ("Name / User ID",  "name_entry",   "e.g. Alice"),
            ("Weight (kg)",     "weight_entry", "20 – 300"),
            ("Height (cm)",     "height_entry", "50 – 250"),
        ]
        self.entries = {}
        for i, (label, attr, placeholder) in enumerate(fields, start=1):
            tk.Label(left, text=label, bg="#16213e", fg="#a0a8c0",
                     font=("Segoe UI", 10)).grid(row=i*2-1, column=0,
                     columnspan=2, sticky="w", pady=(8, 2))
            e = ttk.Entry(left, width=22)
            e.insert(0, placeholder)
            e.bind("<FocusIn>",  lambda ev, ph=placeholder, en=None: self._clear_ph(ev, ph))
            e.bind("<FocusOut>", lambda ev, ph=placeholder: self._restore_ph(ev, ph))
            e.grid(row=i*2, column=0, columnspan=2, sticky="ew", ipady=4)
            self.entries[attr] = e

        ttk.Button(left, text="Calculate BMI", style="Accent.TButton",
                   command=self._calculate).grid(row=10, column=0,
                   columnspan=2, sticky="ew", pady=(20, 4))

        ttk.Button(left, text="Clear", command=self._clear_inputs,
                   style="Accent.TButton").grid(row=11, column=0,
                   columnspan=2, sticky="ew", pady=2)

        # Right panel – result
        right = tk.Frame(outer, bg="#16213e", padx=24, pady=20)
        right.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        tk.Label(right, text="Your BMI Result",
                 bg="#16213e", fg="#e94560",
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")

        self.bmi_value_label = tk.Label(right, text="--",
                                         bg="#16213e", fg="#ffffff",
                                         font=("Segoe UI", 56, "bold"))
        self.bmi_value_label.pack(pady=(10, 0))

        self.category_label = tk.Label(right, text="Enter details to calculate",
                                        bg="#16213e", fg="#a0a8c0",
                                        font=("Segoe UI", 14))
        self.category_label.pack()

        # BMI gauge bar
        self.gauge_canvas = tk.Canvas(right, width=340, height=36,
                                       bg="#16213e", highlightthickness=0)
        self.gauge_canvas.pack(pady=(16, 4))
        self._draw_gauge(None)

        # Tip
        self.tip_label = tk.Label(right, text="",
                                   bg="#16213e", fg="#7f8ea8",
                                   font=("Segoe UI", 9), wraplength=300,
                                   justify="left")
        self.tip_label.pack(anchor="w", pady=(10, 0))

        # Status
        self.status_label = tk.Label(right, text="",
                                      bg="#16213e", fg="#2ecc71",
                                      font=("Segoe UI", 9, "italic"))
        self.status_label.pack(anchor="w", pady=(6, 0))

    def _clear_ph(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)

    def _restore_ph(self, event, placeholder):
        if event.widget.get() == "":
            event.widget.insert(0, placeholder)

    def _draw_gauge(self, bmi_value):
        c = self.gauge_canvas
        c.delete("all")
        w, h = 340, 36
        segments = [(18.5, "#3498db"), (25.0, "#2ecc71"),
                    (30.0, "#f39c12"), (35.0, "#e67e22"),
                    (40.0, "#e74c3c"), (60.0, "#c0392b")]
        bmi_min, bmi_max = 10, 60
        x = 10
        for end, color in segments:
            x2 = 10 + (end - bmi_min) / (bmi_max - bmi_min) * (w - 20)
            c.create_rectangle(x, 14, x2, 28, fill=color, outline="")
            x = x2

        if bmi_value:
            px = 10 + (min(bmi_value, bmi_max) - bmi_min) / (bmi_max - bmi_min) * (w - 20)
            c.create_polygon(px, 4, px-7, 13, px+7, 13, fill="white", outline="")
            c.create_text(px, 34, text=f"{bmi_value}", fill="white",
                          font=("Segoe UI", 8, "bold"))

        labels = ["10", "18.5", "25", "30", "35", "40", "60"]
        for lv in [10, 18.5, 25, 30, 35, 40, 60]:
            lx = 10 + (lv - bmi_min) / (bmi_max - bmi_min) * (w - 20)
            c.create_text(lx, 7, text=str(lv), fill="#7f8ea8",
                          font=("Segoe UI", 7))

    def _calculate(self):
        name   = self.entries["name_entry"].get().strip()
        weight = self.entries["weight_entry"].get().strip()
        height = self.entries["height_entry"].get().strip()

        try:
            if not name or name in ("e.g. Alice",):
                raise ValueError("Please enter a Name / User ID.")
            w = validate_float(weight, "Weight", 20, 300)
            h = validate_float(height, "Height", 50, 250)
            h_m = h / 100
            bmi = calculate_bmi(w, h_m)
            category, color = classify_bmi(bmi)
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return

        # Update UI
        self.bmi_value_label.config(text=str(bmi), fg=color)
        self.category_label.config(text=category, fg=color)
        self._draw_gauge(bmi)

        tips = {
            "Underweight":      "Consider consulting a nutritionist to healthily gain weight.",
            "Normal weight":    "Great job! Maintain your healthy lifestyle.",
            "Overweight":       "Regular exercise and a balanced diet can help.",
            "Obese (Class I)":  "Speak with a healthcare provider for a weight-loss plan.",
            "Obese (Class II)": "Medical guidance is recommended.",
            "Obese (Class III)":"Please consult a doctor as soon as possible.",
        }
        self.tip_label.config(text=tips.get(category, ""))

        # Save record
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if name not in self.data:
            self.data[name] = []
        self.data[name].append({
            "date": timestamp, "weight": w,
            "height": h, "bmi": bmi, "category": category
        })
        save_data(self.data)
        self.status_label.config(text=f"✔ Saved for '{name}'  at {timestamp}")
        self._refresh_history(name)

    def _clear_inputs(self):
        for attr, ph in zip(
            ["name_entry", "weight_entry", "height_entry"],
            ["e.g. Alice", "20 – 300", "50 – 250"]
        ):
            e = self.entries[attr]
            e.delete(0, tk.END)
            e.insert(0, ph)
        self.bmi_value_label.config(text="--", fg="white")
        self.category_label.config(text="Enter details to calculate", fg="#a0a8c0")
        self._draw_gauge(None)
        self.tip_label.config(text="")
        self.status_label.config(text="")

    # ── History Tab ───────────────────────────────────────────────────────────
    def _build_history_tab(self):
        top = tk.Frame(self.tab_history, bg="#1a1a2e")
        top.pack(fill="x", padx=10, pady=(10, 4))

        tk.Label(top, text="User:", bg="#1a1a2e", fg="#a0a8c0").pack(side="left")
        self.user_combo = ttk.Combobox(top, textvariable=self.current_user, width=18)
        self.user_combo['values'] = list(self.data.keys())
        self.user_combo.pack(side="left", padx=6)
        self.user_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_history())

        ttk.Button(top, text="Load", style="Accent.TButton",
                   command=self._refresh_history).pack(side="left", padx=4)
        ttk.Button(top, text="Delete User", style="Accent.TButton",
                   command=self._delete_user).pack(side="left", padx=4)

        if MATPLOTLIB_AVAILABLE:
            ttk.Button(top, text="📈 Trend Graph", style="Accent.TButton",
                       command=self._show_graph).pack(side="left", padx=4)

        # Treeview
        cols = ("Date", "Weight (kg)", "Height (cm)", "BMI", "Category")
        self.tree = ttk.Treeview(self.tab_history, columns=cols,
                                  show="headings", height=16)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120 if c != "Category" else 160, anchor="center")

        sb = ttk.Scrollbar(self.tab_history, orient="vertical",
                           command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=6)
        sb.pack(side="left", fill="y", pady=6)

        self._refresh_history()

    def _refresh_history(self, user=None):
        if user:
            self.current_user.set(user)
        self.user_combo['values'] = list(self.data.keys())
        name = self.current_user.get()
        for row in self.tree.get_children():
            self.tree.delete(row)
        if name in self.data:
            for record in reversed(self.data[name]):
                self.tree.insert("", "end", values=(
                    record["date"], record["weight"],
                    record["height"], record["bmi"], record["category"]
                ))

    def _delete_user(self):
        name = self.current_user.get()
        if name in self.data:
            if messagebox.askyesno("Confirm", f"Delete all data for '{name}'?"):
                del self.data[name]
                save_data(self.data)
                self.current_user.set("")
                self._refresh_history()
        else:
            messagebox.showinfo("Info", "No user selected.")

    def _show_graph(self):
        name = self.current_user.get()
        if name not in self.data or len(self.data[name]) < 2:
            messagebox.showinfo("Info", "Need at least 2 records to show a trend.")
            return

        records = self.data[name]
        dates  = [r["date"] for r in records]
        bmis   = [r["bmi"]  for r in records]
        x      = list(range(len(dates)))

        fig, ax = plt.subplots(figsize=(7, 4), facecolor="#16213e")
        ax.set_facecolor("#0f3460")
        ax.plot(x, bmis, marker="o", color="#e94560", linewidth=2.5,
                markersize=7, markerfacecolor="white")
        for xi, yi in zip(x, bmis):
            ax.annotate(str(yi), (xi, yi), textcoords="offset points",
                        xytext=(0, 8), ha="center", color="white", fontsize=8)

        ax.axhspan(0,    18.5, alpha=0.15, color="#3498db", label="Underweight")
        ax.axhspan(18.5, 25,   alpha=0.15, color="#2ecc71", label="Normal")
        ax.axhspan(25,   30,   alpha=0.15, color="#f39c12", label="Overweight")
        ax.axhspan(30,   50,   alpha=0.15, color="#e74c3c", label="Obese")

        ax.set_xticks(x)
        ax.set_xticklabels([d[:10] for d in dates], rotation=25,
                           ha="right", color="#a0a8c0", fontsize=8)
        ax.set_ylabel("BMI", color="#a0a8c0")
        ax.set_title(f"BMI Trend – {name}", color="#e94560", fontsize=13, fontweight="bold")
        ax.tick_params(colors="#a0a8c0")
        for spine in ax.spines.values():
            spine.set_edgecolor("#0f3460")
        ax.legend(loc="upper right", fontsize=8,
                  facecolor="#16213e", labelcolor="white", edgecolor="#0f3460")

        plt.tight_layout()
        plt.show()

    # ── BMI Info Tab ──────────────────────────────────────────────────────────
    def _build_info_tab(self):
        canvas = tk.Canvas(self.tab_info, bg="#1a1a2e", highlightthickness=0)
        sb = ttk.Scrollbar(self.tab_info, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg="#1a1a2e")

        frame.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        tk.Label(frame, text="BMI Category Reference Guide",
                 bg="#1a1a2e", fg="#e94560",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(16, 8))

        for low, high, label, color in BMI_CATEGORIES:
            row = tk.Frame(frame, bg="#16213e", pady=10, padx=16)
            row.pack(fill="x", padx=20, pady=4)

            tk.Label(row, text="  ", bg=color, width=2).pack(side="left")
            tk.Label(row, text=f"  {label}",
                     bg="#16213e", fg=color,
                     font=("Segoe UI", 11, "bold"), width=20,
                     anchor="w").pack(side="left")
            high_str = f"< {high}" if high < 999 else "≥ 40"
            tk.Label(row, text=f"BMI: {low} – {high_str}",
                     bg="#16213e", fg="#c8d0e0",
                     font=("Segoe UI", 10)).pack(side="left", padx=10)

        tk.Label(frame, text="Formula:  BMI = weight(kg) ÷ height(m)²",
                 bg="#1a1a2e", fg="#a0a8c0",
                 font=("Segoe UI", 10, "italic")).pack(anchor="w", padx=20, pady=(16, 4))

        note = ("Note: BMI is a screening tool, not a diagnostic measure. "
                "Consult a healthcare professional for a complete health assessment.")
        tk.Label(frame, text=note, bg="#1a1a2e", fg="#7f8ea8",
                 font=("Segoe UI", 9), wraplength=480,
                 justify="left").pack(anchor="w", padx=20, pady=(4, 20))


# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = BMIApp()
    app.mainloop()
