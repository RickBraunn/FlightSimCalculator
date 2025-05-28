import tkinter as tk
from tkinter import ttk, messagebox

class FuelCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fuel Calculator")
        self.geometry("500x600")
        self.configure(bg="#f9f9f9")
        self.create_widgets()
        self.show_disclaimer()

    def create_widgets(self):
        # Main container frame
        container = tk.Frame(self, bg="white", padx=20, pady=20)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = tk.Label(container, text="Fuel Calculator", font=("Arial", 24), fg="#007BFF", bg="white")
        header.pack(pady=(0, 10))

        # Learn more label
        learn_more = tk.Label(container, text="*learn more", fg="#333", bg="white", cursor="hand2")
        learn_more.pack(anchor="w")
        learn_more.bind("<Button-1>", lambda e: self.show_info())

        # Fuel mode selection
        fuel_mode_frame = tk.Frame(container, bg="white")
        fuel_mode_frame.pack(fill="x", pady=10)
        tk.Label(fuel_mode_frame, text="Select Fuel Calculation Mode:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.fuel_mode_var = tk.StringVar(value="faa")
        fuel_mode_dropdown = ttk.Combobox(fuel_mode_frame, textvariable=self.fuel_mode_var, state="readonly",
                                          values=["faa", "custom"])
        fuel_mode_dropdown.pack(fill="x")
        fuel_mode_dropdown.bind("<<ComboboxSelected>>", lambda e: self.toggle_inputs())

        # Custom inputs frame
        self.custom_inputs_frame = tk.Frame(container, bg="white")
        self.custom_inputs_frame.pack(fill="x", pady=10)

        tk.Label(self.custom_inputs_frame, text="Contingency (%):", bg="white").grid(row=0, column=0, sticky="w")
        self.contingency_var = tk.DoubleVar(value=5.0)
        tk.Entry(self.custom_inputs_frame, textvariable=self.contingency_var, width=10).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(self.custom_inputs_frame, text="Reserve Minutes:", bg="white").grid(row=0, column=2, sticky="w", padx=(20,0))
        self.reserve_minutes_var = tk.IntVar(value=45)
        tk.Entry(self.custom_inputs_frame, textvariable=self.reserve_minutes_var, width=10).grid(row=0, column=3, sticky="w", padx=5)

        # Flight type frame
        self.flight_type_frame = tk.Frame(container, bg="white")
        self.flight_type_frame.pack(fill="x", pady=10)
        tk.Label(self.flight_type_frame, text="Select Flight Type:", bg="white").pack(anchor="w")
        self.flight_type_var = tk.StringVar(value="VFR")
        flight_type_dropdown = ttk.Combobox(self.flight_type_frame, textvariable=self.flight_type_var, state="readonly",
                                            values=["VFR", "IFR"])
        flight_type_dropdown.pack(fill="x")

        # Input fields
        self.inputs_frame = tk.Frame(container, bg="white")
        self.inputs_frame.pack(fill="x", pady=10)

        labels = [
            "A to B distance (nm):",
            "B to C distance (nm):",
            "Average cruise speed (kts):",
            "Average fuel consumption (usg/hr):",
            "Average headwind (kts):"
        ]
        self.input_vars = []
        for i, label_text in enumerate(labels):
            tk.Label(self.inputs_frame, text=label_text, bg="white").grid(row=i, column=0, sticky="w", pady=5)
            var = tk.DoubleVar()
            entry = tk.Entry(self.inputs_frame, textvariable=var)
            entry.grid(row=i, column=1, sticky="w", pady=5, padx=5)
            self.input_vars.append(var)

        # Calculate button
        calc_button = tk.Button(container, text="Calculate Fuel", bg="#007BFF", fg="white", font=("Arial", 12, "bold"),
                                command=self.calculate_fuel)
        calc_button.pack(pady=15, fill="x")

        # Result label
        self.result_label = tk.Label(container, text="", bg="white", font=("Arial", 14), relief="solid", bd=1, padx=10, pady=10)
        self.result_label.pack(fill="x")

        self.toggle_inputs()

    def show_disclaimer(self):
        messagebox.showinfo("Disclaimer", "This fuel calculator is designed exclusively for flight simulation purposes. "
                                          "It is not intended for actual flight planning or navigation. "
                                          "Please consult official resources and professionals for real-world flight operations.")

    def show_info(self):
        messagebox.showinfo("Info", "This calculator currently uses 5% fuel for contingency and 45 minutes for final reserve. "
                                    "In the future, it will match the FAA fuel requirements.")

    def toggle_inputs(self):
        mode = self.fuel_mode_var.get()
        if mode == "custom":
            self.custom_inputs_frame.pack(fill="x", pady=10)
            self.flight_type_frame.pack_forget()
        elif mode == "faa":
            self.custom_inputs_frame.pack_forget()
            self.flight_type_frame.pack(fill="x", pady=10)
        else:
            self.custom_inputs_frame.pack_forget()
            self.flight_type_frame.pack_forget()

    def calculate_fuel(self):
        try:
            distance_ab = self.input_vars[0].get()
            distance_bc = self.input_vars[1].get()
            cruise_speed = self.input_vars[2].get()
            fuel_consumption = self.input_vars[3].get()
            headwind = self.input_vars[4].get()

            if distance_ab < 0 or distance_bc < 0 or cruise_speed <= 0 or fuel_consumption <= 0 or headwind < 0:
                self.result_label.config(text="Please enter valid positive numbers for all inputs.")
                return

            mode = self.fuel_mode_var.get()
            if mode == "custom":
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

            if mode == "custom":
                total_fuel_ab = calculate_leg_fuel(distance_ab, speed, fuel_consumption, contingency_percent)
                total_fuel_bc = calculate_leg_fuel(distance_bc, speed, fuel_consumption, contingency_percent)
                total_trip_fuel = total_fuel_ab + total_fuel_bc
                reserve_fuel = (reserve_minutes / 60) * fuel_consumption
            elif mode == "faa":
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

            total_fuel_required = total_trip_fuel + reserve_fuel
            self.result_label.config(text=f"Total Fuel Required: {total_fuel_required:.2f} gallons")

        except tk.TclError:
            self.result_label.config(text="Please enter valid numbers in all fields.")

if __name__ == "__main__":
    app = FuelCalculatorApp()
    app.mainloop()
