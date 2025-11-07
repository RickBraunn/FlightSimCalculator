import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import os

class FuelCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fuel Calculator")
        self.state('zoomed')  # Maximize window on start
        self.configure(bg="#1E2A38")  # Dark aviation blue background
        from tkinter.font import Font
        self.custom_font = Font(family="Segoe UI", size=12)
        self.header_font = Font(family="Segoe UI", size=28, weight="bold")
        self.result_font = Font(family="Segoe UI", size=14, weight="bold")
        self.create_widgets()
        self.show_disclaimer()

    def create_widgets(self):
        # Main container frame
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)
        container.configure(style="Container.TFrame")

        # Header with icon and text
        header_frame = ttk.Frame(container)
        header_frame.grid(row=0, column=0, columnspan=4, pady=(0, 15), sticky="w")

        # Load airplane icon
        import os
        from PIL import Image, ImageTk
        icon_path = os.path.join(os.path.dirname(__file__), "airplane_icon.png")
        try:
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((40, 40), Image.ANTIALIAS)
            self.airplane_icon = ImageTk.PhotoImage(icon_image)
        except Exception:
            self.airplane_icon = None

        if self.airplane_icon:
            icon_label = ttk.Label(header_frame, image=self.airplane_icon)
            icon_label.pack(side="left", padx=(0, 10))

        header = ttk.Label(header_frame, text="Fuel Calculator", font=self.header_font, foreground="#00A3E0")
        header.pack(side="left")

        # Unit selection
        unit_frame = ttk.Frame(container)
        unit_frame.grid(row=1, column=0, columnspan=4, sticky="w", pady=(5, 0))
        ttk.Label(unit_frame, text="Select Unit:", font=self.custom_font, foreground="#FFFFFF").pack(side="left", padx=(0, 10))
        self.unit_var = tk.StringVar(value="USG")
        units = [("USG", "USG"), ("LBS", "LBS"), ("L", "L"), ("KG", "KG")]
        for text, value in units:
            rb = tk.Radiobutton(unit_frame, text=text, variable=self.unit_var, value=value, font=self.custom_font, bg="#1E2A38", fg="#FFFFFF", selectcolor="#1E2A38", activebackground="#1E2A38", activeforeground="#FFFFFF")
            rb.pack(side="left", padx=(0, 10))
            rb.bind("<Button-1>", lambda e, v=value: self.update_fuel_label(v))

        # Fuel mode selection
        ttk.Label(container, text="Select Fuel Calculation Mode:", font=self.custom_font, foreground="#FFFFFF").grid(row=2, column=0, sticky="w", pady=(15, 5))
        self.fuel_mode_var = tk.StringVar(value="FAA Fuel Requirements")
        self.fuel_mode_dropdown = ttk.Combobox(container, textvariable=self.fuel_mode_var, state="readonly", values=["FAA Fuel Requirements", "Custom Fuel"], font=self.custom_font)
        self.fuel_mode_dropdown.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.fuel_mode_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_mode())

        # Custom inputs frame
        custom_frame = ttk.LabelFrame(container, text="Custom Inputs", style="Custom.TLabelframe")
        custom_frame.grid(row=4, column=0, columnspan=4, sticky="ew", pady=15)

        ttk.Label(custom_frame, text="Contingency (%):", font=self.custom_font).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.contingency_var = tk.DoubleVar(value=5.0)
        self.contingency_entry = ttk.Entry(custom_frame, textvariable=self.contingency_var, width=15, font=self.custom_font)
        self.contingency_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(custom_frame, text="Reserve Minutes:", font=self.custom_font).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.reserve_minutes_var = tk.IntVar(value=45)
        self.reserve_entry = ttk.Entry(custom_frame, textvariable=self.reserve_minutes_var, width=15, font=self.custom_font)
        self.reserve_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)

        # Flight type selection
        flight_type_frame = ttk.LabelFrame(container, text="Flight Type")
        flight_type_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

        ttk.Label(flight_type_frame, text="Select Flight Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.flight_type_var = tk.StringVar(value="Select Flight Rule")
        self.flight_type_dropdown = ttk.Combobox(flight_type_frame, textvariable=self.flight_type_var, state="readonly", values=["Select Flight Rule", "VFR", "IFR"])
        self.flight_type_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Flight parameters frame
        params_frame = ttk.LabelFrame(container, text="Flight Parameters")
        params_frame.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10)

        # Create a StringVar for the dynamic fuel consumption label
        self.fuel_label_var = tk.StringVar(value=f"Average fuel consumption ({self.unit_var.get()}/hr):")

        labels = [
            "A to B distance (nm):",
            "B to C distance (nm):",
            "Taxi time (minutes):",
            "Average cruise speed (kts):",
            None,  # Placeholder for fuel consumption label
            "Average headwind (kts):"
        ]
        self.input_vars = []
        for i, label_text in enumerate(labels):
            if i == 4:  # Fuel consumption label
                ttk.Label(params_frame, textvariable=self.fuel_label_var).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            else:
                ttk.Label(params_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value="0" if label_text == "Taxi time (minutes):" else "")
            entry = ttk.Entry(params_frame, textvariable=var)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.input_vars.append(var)

        # Configure grid weights for params_frame
        params_frame.columnconfigure(1, weight=1)

        # Calculate button
        self.calc_button = ttk.Button(container, text="Calculate Fuel", command=self.calculate_fuel, style="Calc.TButton")
        self.calc_button.grid(row=7, column=0, columnspan=4, sticky="ew", pady=20)

        # Result label
        self.result_label = ttk.Label(container, text="", background="#FFFFFF", font=self.result_font, relief="solid", padding=10)
        self.result_label.grid(row=8, column=0, columnspan=4, sticky="ew")

        # Initialize mode states
        self.update_mode()
        # Add forced multiple update_mode calls to fix UI glitch
        self.after(100, self.update_mode)
        self.after(300, self.update_mode)
        self.after(500, self.update_mode)

    def show_disclaimer(self):
        messagebox.showinfo("Disclaimer", "This fuel calculator is designed exclusively for flight simulation purposes. "
                                          "It is not intended for actual flight planning or navigation. "
                                          "Please consult official resources and professionals for real-world flight operations.")

    def show_info(self):
        messagebox.showinfo("Info", "This calculator currently uses 5% fuel for contingency and 45 minutes for final reserve. "
                                    "In the future, it will match the FAA fuel requirements.")

    def update_mode(self):
        mode = self.fuel_mode_var.get()
        if mode == "Custom Fuel":
            self.contingency_entry.config(state="normal")
            self.reserve_entry.config(state="normal")
            self.flight_type_dropdown.config(state="disabled")
        elif mode == "FAA Fuel Requirements":
            self.contingency_entry.config(state="disabled")
            self.reserve_entry.config(state="disabled")
            self.flight_type_dropdown.config(state="readonly")
        else:
            self.contingency_entry.config(state="disabled")
            self.reserve_entry.config(state="disabled")
            self.flight_type_dropdown.config(state="disabled")

    def update_fuel_label(self, unit):
        # Update the fuel consumption label dynamically
        self.fuel_label_var.set(f"Average fuel consumption ({unit}/hr):")

    def calculate_fuel(self):
        try:
            distance_ab = float(self.input_vars[0].get())
            distance_bc = float(self.input_vars[1].get())
            taxi_time = float(self.input_vars[2].get())
            cruise_speed = float(self.input_vars[3].get())
            fuel_consumption_input = float(self.input_vars[4].get())
            headwind = float(self.input_vars[5].get())
            selected_unit = self.unit_var.get()

            # Validate inputs
            if any(val < 0 for val in [distance_ab, distance_bc, headwind, taxi_time]) or cruise_speed <= 0 or fuel_consumption_input <= 0:
                self.result_label.config(text="Please enter valid positive numbers for all inputs.")
                return

            # Convert fuel consumption to USG/hr for calculation
            fuel_consumption = fuel_consumption_input
            if selected_unit == 'LBS':
                fuel_consumption = fuel_consumption_input / 6.7  # LBS to USG
            elif selected_unit == 'L':
                fuel_consumption = fuel_consumption_input / 3.785  # L to USG
            elif selected_unit == 'KG':
                fuel_consumption = fuel_consumption_input / 3.04  # KG to USG
            # USG remains as is

            mode = self.fuel_mode_var.get()
            if mode.lower() == "custom":
                contingency_percent = self.contingency_var.get()
                reserve_minutes = self.reserve_minutes_var.get()
                if contingency_percent < 0 or reserve_minutes < 0:
                    self.result_label.config(text="Please enter valid positive numbers for contingency and reserve.")
                    return
            else:
                contingency_percent = 5
                reserve_minutes = 45

            speed = cruise_speed - headwind
            if speed <= 0:
                self.result_label.config(text="Effective speed must be greater than zero. Please check cruise speed and headwind values.")
                return

            def calculate_leg_fuel(distance, speed, consumption, buffer_percent):
                time = distance / speed
                fuel = time * consumption
                return fuel * (1 + buffer_percent / 100)

            total_trip_fuel = 0
            reserve_fuel = 0

            if mode.lower() == "custom":
                total_fuel_ab = calculate_leg_fuel(distance_ab, speed, fuel_consumption, contingency_percent)
                total_fuel_bc = calculate_leg_fuel(distance_bc, speed, fuel_consumption, contingency_percent)
                total_trip_fuel = total_fuel_ab + total_fuel_bc
                reserve_fuel = (reserve_minutes / 60) * fuel_consumption
            elif mode.lower() == "faa fuel requirements":
                flight_type = self.flight_type_var.get()
                if flight_type == "IFR":
                    trip_fuel_ab = calculate_leg_fuel(distance_ab, speed, fuel_consumption, 0)
                    trip_fuel_bc = calculate_leg_fuel(distance_bc, speed, fuel_consumption, 0)
                    trip_fuel = trip_fuel_ab + trip_fuel_bc
                    alternate_fuel = trip_fuel * 0.10
                    reserve = (45 / 60) * fuel_consumption
                    total_trip_fuel = trip_fuel + alternate_fuel
                    reserve_fuel = reserve
                elif flight_type == "VFR":
                    trip_fuel_ab = calculate_leg_fuel(distance_ab, speed, fuel_consumption, 0)
                    trip_fuel_bc = calculate_leg_fuel(distance_bc, speed, fuel_consumption, 0)
                    total_trip_fuel = trip_fuel_ab + trip_fuel_bc
                    reserve_fuel = (30 / 60) * fuel_consumption
                else:
                    total_fuel_ab = calculate_leg_fuel(distance_ab, speed, fuel_consumption, 10)
                    total_fuel_bc = calculate_leg_fuel(distance_bc, speed, fuel_consumption, 10)
                    total_trip_fuel = total_fuel_ab + total_fuel_bc
                    reserve_fuel = (45 / 60) * fuel_consumption

            taxi_fuel = (taxi_time / 60) * fuel_consumption
            total_fuel_required = total_trip_fuel + reserve_fuel + taxi_fuel

            # Convert total fuel back to selected unit for display
            unit_name = 'gallons'
            if selected_unit == 'LBS':
                total_fuel_required *= 6.7  # USG to LBS
                unit_name = 'lbs'
            elif selected_unit == 'L':
                total_fuel_required *= 3.785  # USG to L
                unit_name = 'liters'
            elif selected_unit == 'KG':
                total_fuel_required *= 3.04  # USG to KG
                unit_name = 'kg'
            # USG remains as gallons

            self.result_label.config(text=f"Total Fuel Required: {total_fuel_required:.2f} {unit_name}")

        except ValueError:
            self.result_label.config(text="Please enter valid numbers in all fields.")

if __name__ == "__main__":
    app = FuelCalculatorApp()
    app.mainloop()
