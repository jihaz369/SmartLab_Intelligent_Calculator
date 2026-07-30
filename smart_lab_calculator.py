# SmartLab_Intelligent_Calc.py
# AI-assisted intelligent lab calculator for LEDs, MOSFETs, and circuits

import math

def get_numbered_choice(prompt, options):
    print(prompt)
    for i, opt in enumerate(options, start=1):
        print(f"  {i} - {opt}")
    while True:
        choice = input(f"Enter choice (1-{len(options)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        else:
            print("Invalid input, enter a number from the list.")

def led_calculator():
    print("\n=== Intelligent LED Module ===")
    V_source = float(input("Enter supply voltage (V): ").replace("V",""))
    Vf = float(input("Enter LED forward voltage (Vf): ").replace("V",""))
    I_led_mA = float(input("Enter desired LED current (mA): "))
    R_series = (V_source - Vf) / (I_led_mA/1000)
    print(f"- Suggested series resistor: {R_series:.2f} Ω")
    print(f"- Expected current: {I_led_mA} mA")
    print("- Polarity: Anode → +, Cathode → -")
    if R_series < 10:
        print("⚠ Warning: resistor very small, consider using higher supply voltage or limiting current differently")
    print("- Optional: 10-100nF capacitor across LED if PWM used")

def mosfet_calculator():
    print("\n=== Intelligent MOSFET Module ===")
    mos_type = input("Enter MOSFET type (N or P): ").strip().upper()
    Vds_max = float(input("Enter Vds max (V): ").replace("V",""))
    Id_max = float(input("Enter Id max (A): ").replace("A",""))
    Rds_on_input = input("Enter Rds(on) Ω (leave blank if unknown): ").strip()
    Rds_on = float(Rds_on_input) if Rds_on_input else None
    Vgs_th = float(input("Enter gate threshold Vgs(th) (V): ").replace("V",""))
    V_source = float(input("Enter supply voltage (V): ").replace("V",""))
    I_load = float(input("Enter desired load current (A): ").replace("A",""))
    Cgs_nF = float(input("Enter MOSFET input capacitance Cgs (nF): "))
    V_drive = float(input("Enter gate drive voltage (V): "))
    desired_gate_time_us = float(input("Desired gate switching time (μs): "))

    # Intelligent calculations
    print("\n--- MOSFET Analysis ---")
    if V_source >= Vds_max * 0.8:
        print("⚠ Warning: Supply voltage close to MOSFET Vds max")
    if I_load >= Id_max * 0.8:
        print("⚠ Warning: Load current close to MOSFET Id max")

    if Rds_on:
        P_diss = I_load**2 * Rds_on
        print(f"- Estimated MOSFET dissipation: {P_diss:.2f} W")
        if P_diss > 0.5:
            print("- Heatsink recommended")

    # Gate resistor calculation
    R_gate = (V_drive * desired_gate_time_us * 1e-6) / (Cgs_nF * 1e-9)
    print(f"- Suggested gate resistor: {R_gate:.1f} Ω for {desired_gate_time_us} μs switching")

    # Select cases
    cases = ["Inductive load", "High-speed switching", "Sensitive circuit",
             "Transformer/flyback", "DC-DC boost/upconverter", "Heavy load/high power"]
    selected_cases = get_numbered_choice("Select primary circuit case:", cases)

    # Intelligent suggestions
    print("\n--- Intelligent Recommendations ---")
    if selected_cases == 1:
        sub_options = ["DC Motor", "Relay", "Solenoid", "Transformer winding 30V"]
        sub_choice = get_numbered_choice("Select inductive load type:", sub_options)
        if sub_choice == 1:
            R_snubber = max(V_source/I_load, 1)
            print(f"- DC Motor: Flyback diode recommended")
            print(f"- Suggested snubber resistor: {R_snubber:.1f} Ω, consider 0.25-1W rating")
        elif sub_choice == 4:
            R_snubber = max(V_source/I_load, 1)
            C_snubber_nF = 10  # example default
            print("- Transformer winding: RC snubber recommended")
            print(f"- Suggested resistor: {R_snubber:.1f} Ω, Capacitor: {C_snubber_nF} nF")
    elif selected_cases == 5:
        R_current = V_source / I_load
        print(f"- DC-DC boost: optional input/output series resistor {R_current:.1f} Ω")
    else:
        print("- Standard protection components suggested based on case")

    print("\n--- Lab Safety Tips ---")
    print("- Start with low voltage/current")
    print("- Verify wiring and MOSFET orientation")
    print("- Use multimeter/oscilloscope to monitor voltage and current")
    print("- Add fuses where appropriate")

def main():
    print("=== SmartLab Intelligent Universal Calculator ===")
    modules = ["LED & Diode", "MOSFET"]
    choice = get_numbered_choice("Select module:", modules)
    if choice == 1:
        led_calculator()
    elif choice == 2:
        mosfet_calculator()

if __name__ == "__main__":
    main()
