import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk
import os

class FuelCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fuel Calculator")
        self.configure(bg="#1E2A38")  # Dark aviation blue background
        from tkinter.font import Font
        self.custom_font = Font(family="Segoe UI", size=12)
        self.header_font = Font(family="Segoe UI", size=28, weight="bold")
        self.result_font = Font(family="Segoe UI", size=14, weight="bold")
        self.setup_styles()
        self.create_widgets()
        # Set window size to fit the entire application
        self.update_idletasks()
        self.req_width = self.winfo_reqwidth()
        self.req_height = self.winfo_reqheight()
        self.geometry(f'{self.req_width}x{self.req_height}')
        # Center the window on screen
        x = (self.winfo_screenwidth() // 2) - (self.req_width // 2)
        y = (self.winfo_screenheight() // 2) - (self.req_height // 2)
        self.geometry(f'{self.req_width}x{self.req_height}+{x}+{y}')
        # Bind to configure event to handle full screen changes
        self.bind('<Configure>', self.on_resize)
        self.show_disclaimer()

    def setup_styles(self):
        # Set theme to 'clam' for modern look
        style = ttk.Style()
        style.theme_use('clam')

        # Define custom styles using Flight Simulator colors
        # Background: #1E2A38 (dark blue), Accent: #00A3E0 (blue), Text: #FFFFFF (white)

        # Frame styles
        style.configure("Container.TFrame", background="#1E2A38")
        style.configure("Custom.TLabelframe", background="#1E2A38", foreground="#FFFFFF", borderwidth=2, relief="groove")
        style.configure("Custom.TLabelframe.Label", background="#1E2A38", foreground="#00A3E0", font=self.custom_font)

        # Label styles
        style.configure("TLabel", background="#1E2A38", foreground="#FFFFFF", font=self.custom_font)

        # Entry styles
        style.configure("TEntry", fieldbackground="#2A3A4A", bordercolor="#00A3E0", lightcolor="#00A3E0", darkcolor="#00A3E0", insertcolor="#FFFFFF", foreground="#FFFFFF", font=self.custom_font)

        # Button styles
        style.configure("Calc.TButton", background="#00A3E0", foreground="#FFFFFF", font=self.custom_font, padding=10, relief="raised")
        style.map("Calc.TButton", background=[("active", "#007ACC")])

        # Combobox styles
        style.configure("TCombobox", fieldbackground="#2A3A4A", background="#1E2A38", foreground="#FFFFFF", arrowcolor="#00A3E0", bordercolor="#00A3E0", lightcolor="#00A3E0", darkcolor="#00A3E0", font=self.custom_font)
        style.map("TCombobox", fieldbackground=[("readonly", "#2A3A4A")], background=[("readonly", "#1E2A38")])

    def create_widgets(self):
        # Main container frame
        self.container = ttk.Frame(self, padding=20)
        self.container.pack(fill="both", expand=True)
        self.container.configure(style="Container.TFrame")

        # Header with icon and text
        header_frame = ttk.Frame(self.container)
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



        # Fuel mode selection
        ttk.Label(self.container, text="Select Fuel Calculation Mode:", font=self.custom_font, foreground="#FFFFFF").grid(row=2, column=0, sticky="w", pady=(15, 5))
        self.fuel_mode_var = tk.StringVar(value="FAA Fuel Requirements")
        self.fuel_mode_dropdown = ttk.Combobox(self.container, textvariable=self.fuel_mode_var, state="readonly", values=["FAA Fuel Requirements", "Custom Fuel"], font=self.custom_font)
        self.fuel_mode_dropdown.grid(row=3, column=0, columnspan=4, sticky="ew")
        self.fuel_mode_dropdown.bind("<<ComboboxSelected>>", lambda e: self.update_mode())

        # Custom inputs frame
        custom_frame = ttk.LabelFrame(self.container, text="Custom Inputs", style="Custom.TLabelframe")
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
        flight_type_frame = ttk.LabelFrame(self.container, text="Flight Type", style="Custom.TLabelframe")
        flight_type_frame.grid(row=5, column=0, columnspan=4, sticky="ew", pady=10)

        ttk.Label(flight_type_frame, text="Select Flight Type:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.flight_type_var = tk.StringVar(value="Select Flight Rule")
        self.flight_type_dropdown = ttk.Combobox(flight_type_frame, textvariable=self.flight_type_var, state="readonly", values=["Select Flight Rule", "VFR", "IFR"])
        self.flight_type_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Flight parameters frame
        params_frame = ttk.LabelFrame(self.container, text="Flight Parameters", style="Custom.TLabelframe")
        params_frame.grid(row=6, column=0, columnspan=4, sticky="ew", pady=10)

        # Create a StringVar for the dynamic fuel consumption label
        self.fuel_label_var = tk.StringVar(value="Average fuel consumption (USG/hr):")

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
                # Add fuel consumption unit combobox next to the entry
                self.fuel_consumption_unit_var = tk.StringVar(value="USG")
                self.fuel_consumption_unit_combobox = ttk.Combobox(params_frame, textvariable=self.fuel_consumption_unit_var, state="readonly", values=["USG", "LBS", "L", "KG"], width=5)
                self.fuel_consumption_unit_combobox.grid(row=i, column=2, sticky="w", padx=5, pady=5)
                self.fuel_consumption_unit_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_fuel_label_and_convert(self.fuel_consumption_unit_var.get()))
            else:
                ttk.Label(params_frame, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value="")
            entry = ttk.Entry(params_frame, textvariable=var)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
            self.input_vars.append(var)

        # Configure grid weights for params_frame
        params_frame.columnconfigure(1, weight=1)

        # Result unit selection
        ttk.Label(self.container, text="Result Unit:", font=self.custom_font).grid(row=7, column=0, sticky="w", pady=(10, 5))
        self.result_unit_var = tk.StringVar(value="USG")
        self.result_unit_combobox = ttk.Combobox(self.container, textvariable=self.result_unit_var, state="readonly", values=["USG", "LBS", "L", "KG"], font=self.custom_font, width=10)
        self.result_unit_combobox.grid(row=7, column=1, sticky="w", pady=(10, 5))
        self.result_unit_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_result_display())

        # Calculate button
        self.calc_button = ttk.Button(self.container, text="Calculate Fuel", command=self.calculate_fuel, style="Calc.TButton")
        self.calc_button.grid(row=8, column=0, columnspan=4, sticky="ew", pady=20)

        # Result label
        self.result_label = ttk.Label(self.container, text="", background="#2A3A4A", foreground="#00A3E0", font=self.result_font, relief="groove", borderwidth=2, padding=10)
        self.result_label.grid(row=9, column=0, columnspan=4, sticky="ew")

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

    def on_resize(self, event):
        # Check if the window is maximized
        if self.state() == 'zoomed':
            # Maximized: center the container at its normal size
            self.container.pack_forget()
            self.container.place(relx=0.5, rely=0.5, anchor="center", width=self.req_width, height=self.req_height)
        else:
            # Normal mode: fill the window
            self.container.place_forget()
            self.container.pack(fill="both", expand=True)

    def update_fuel_label(self, unit):
        # Update the fuel consumption label dynamically
        self.fuel_label_var.set(f"Average fuel consumption ({unit}/hr):")

    def update_fuel_label_and_convert(self, unit):
        # Update label and convert fuel consumption value in real-time
        self.update_fuel_label(unit)
        self.convert_fuel_consumption(unit)

    def convert_fuel_consumption(self, new_unit):
        # Convert the fuel consumption value when unit changes
        try:
            current_value = float(self.input_vars[4].get())
            if current_value <= 0:
                return
            # Convert from previous unit to USG
            previous_unit = getattr(self, 'previous_fuel_unit', 'USG')
            value_in_usg = current_value
            if previous_unit == 'LBS':
                value_in_usg = current_value / 6.7
            elif previous_unit == 'L':
                value_in_usg = current_value / 3.785
            elif previous_unit == 'KG':
                value_in_usg = current_value / 3.04
            # Convert to new unit
            new_value = value_in_usg
            if new_unit == 'LBS':
                new_value = value_in_usg * 6.7
            elif new_unit == 'L':
                new_value = value_in_usg * 3.785
            elif new_unit == 'KG':
                new_value = value_in_usg * 3.04
            self.input_vars[4].set(f"{new_value:.2f}")
            self.previous_fuel_unit = new_unit
        except ValueError:
            pass  # Ignore if not a number

    def update_result_display(self):
        # Update result display when result unit changes
        if hasattr(self, 'last_calculated_fuel_usg'):
            result_unit = self.result_unit_var.get()
            total_fuel_required = self.last_calculated_fuel_usg
            unit_name = 'gallons'
            if result_unit == 'LBS':
                total_fuel_required *= 6.7
                unit_name = 'lbs'
            elif result_unit == 'L':
                total_fuel_required *= 3.785
                unit_name = 'liters'
            elif result_unit == 'KG':
                total_fuel_required *= 3.04
                unit_name = 'kg'
            self.result_label.config(text=f"Total Fuel Required: {total_fuel_required:.2f} {unit_name}\nEstimated Time A to B: {self.last_calculated_time_hours} hours {self.last_calculated_time_minutes} minutes")

    def calculate_fuel(self):
        try:
            distance_ab = float(self.input_vars[0].get())
            distance_bc = float(self.input_vars[1].get())
            taxi_time = float(self.input_vars[2].get())
            cruise_speed = float(self.input_vars[3].get())
            fuel_consumption_input = float(self.input_vars[4].get())
            headwind = float(self.input_vars[5].get())
            fuel_consumption_unit = self.fuel_consumption_unit_var.get()
            result_unit = self.result_unit_var.get()

            # Validate inputs
            if any(val < 0 for val in [distance_ab, distance_bc, headwind, taxi_time]) or cruise_speed <= 0 or fuel_consumption_input <= 0:
                self.result_label.config(text="Please enter valid positive numbers for all inputs.")
                return

            # Convert fuel consumption to USG/hr for calculation
            fuel_consumption = fuel_consumption_input
            if fuel_consumption_unit == 'LBS':
                fuel_consumption = fuel_consumption_input / 6.7  # LBS to USG
            elif fuel_consumption_unit == 'L':
                fuel_consumption = fuel_consumption_input / 3.785  # L to USG
            elif fuel_consumption_unit == 'KG':
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

            # Calculate estimated time A to B
            time_hours = distance_ab / speed
            hours = int(time_hours)
            minutes = round((time_hours - hours) * 60)

            # Store the calculated fuel in USG for later unit conversion
            self.last_calculated_fuel_usg = total_fuel_required
            self.last_calculated_time_hours = hours
            self.last_calculated_time_minutes = minutes

            # Convert total fuel back to selected result unit for display
            unit_name = 'gallons'
            if result_unit == 'LBS':
                total_fuel_required *= 6.7  # USG to LBS
                unit_name = 'lbs'
            elif result_unit == 'L':
                total_fuel_required *= 3.785  # USG to L
                unit_name = 'liters'
            elif result_unit == 'KG':
                total_fuel_required *= 3.04  # USG to KG
                unit_name = 'kg'
            # USG remains as gallons

            self.result_label.config(text=f"Total Fuel Required: {total_fuel_required:.2f} {unit_name}\nEstimated Time A to B: {hours} hours {minutes} minutes")

        except ValueError:
            self.result_label.config(text="Please enter valid numbers in all fields.")

if __name__ == "__main__":
    app = FuelCalculatorApp()
    app.mainloop()
