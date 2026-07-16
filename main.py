import os
from ai_brain import generate_tt, review_tt, analyze_tt, analyze_progress, generate_holistic_plan
from csv_utils import log_daily_health

DATA_DIR = "data"
TT_OUTPUT_FILE = os.path.join(DATA_DIR, "my_tt.csv")
HEALTH_LOG_FILE = os.path.join(DATA_DIR, "health_log.csv")

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_choice(prompt_str, valid_options):
    while True:
        val = input(prompt_str).strip().lower()
        if val in valid_options:
            return val
        print(f"❌ Invalid choice. Please choose from: {', '.join(valid_options)}")

def calculate_tdee(weight_kg: float, height_cm: float, age: int, gender: str, activity_level: float) -> dict:
    if gender.lower() == 'm':
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161
        
    tdee = bmr * activity_level
    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "maintenance": round(tdee),
        "cutting": round(tdee - 500),
        "bulking": round(tdee + 300)
    }

def menu():
    print("\n==================================")
    print(" 🛠️ TERMINAL HEALTH ENGINE (v1.0)")
    print("==================================")
    print("--- Training Templates ---")
    print("1. AI Create TT")
    print("2. Review TT (Text)")
    print("3. Analyze TT (JSON Score)")
    print("--- Daily Engine ---")
    print("4. Calculate TDEE/Macros")
    print("5. Log Daily Health Snapshot")
    print("6. AI Analyze Health Log")
    print("7. Generate Holistic Day Plan (Hostel Diet)")
    print("8. Exit")
    return input("\n> Select option: ").strip()

def handle_create_tt():
    print("\n--- AI TT Generator ---")
    user_data = {
        "goal": get_choice("Goal (muscle / fatloss / strength): ", ["muscle", "fatloss", "strength"]),
        "experience": get_choice("Experience (beginner / intermediate): ", ["beginner", "intermediate"]),
        "days": input("Days per week (3–6): ").strip(),
        "time": input("Time per session (minutes): ").strip(),
        "injuries": input("Injuries (or none): ").strip(),
    }
    print("\nGenerating template...")
    csv_text = generate_tt(user_data)
    if not csv_text: return print("Failed to generate TT.")
    
    ensure_data_dir()
    with open(TT_OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("day,exercise,sets,reps,rest_seconds,notes\n" + csv_text)
    print(f"✅ TT saved to: {TT_OUTPUT_FILE}")

def handle_review_tt():
    if not os.path.exists(TT_OUTPUT_FILE): return print("❌ No TT found. Generate one first.")
    with open(TT_OUTPUT_FILE, "r", encoding="utf-8") as f:
        print("\n" + review_tt(f.read()))

def handle_analyze_tt():
    if not os.path.exists(TT_OUTPUT_FILE): return print("❌ No TT found.")
    with open(TT_OUTPUT_FILE, "r", encoding="utf-8") as f:
        print("\n" + str(analyze_tt(f.read())))

def handle_tdee():
    print("\n--- TDEE Calculator ---")
    try:
        w = float(input("Weight (kg): "))
        h = float(input("Height (cm): "))
        a = int(input("Age: "))
        g = get_choice("Gender (M/F): ", ["m", "f"])
        act = float(input("Activity Multiplier (1.2 sedentary -> 1.9 athlete): "))
        res = calculate_tdee(w, h, a, g, act)
        print("\n--- Output ---")
        for k, v in res.items(): print(f"{k.capitalize()}: {v} kcal")
    except ValueError:
        print("❌ Invalid number entered.")

def handle_log_health():
    print("\n--- Log Health Snapshot ---")
    ensure_data_dir()
    
    # Safely get weight
    w_input = input("Current Weight (kg) [or 'idk']: ").strip().lower()
    w = 0.0 if w_input in ['idk', '?', ''] else float(w_input)
    
    # Safely get sleep
    s_input = input("Sleep last night (hours) [or 'idk']: ").strip().lower()
    s = 0.0 if s_input in ['idk', '?', ''] else float(s_input)
    
    # Safely get calories
    c_input = input("Calories consumed today (approx) [or 'idk']: ").strip().lower()
    c = 0 if c_input in ['idk', '?', ''] else int(c_input)
    
    wk = get_choice("Did you workout today? (y/n): ", ["y", "n"]) == "y"
    n = input("Notes (optional): ").strip()
    
    log_daily_health(w, s, c, wk, n)
    print("✅ Log saved successfully.")

def handle_analyze_log():
    if not os.path.exists(HEALTH_LOG_FILE): return print("❌ No health log found. Log some data first.")
    print("\nAnalyzing recent health data...")
    with open(HEALTH_LOG_FILE, "r", encoding="utf-8") as f:
        print("\n" + str(analyze_progress(f.read())))

def handle_holistic_plan():
    print("\n--- Generate Daily Plan ---")
    goal = input("Current Goal (e.g., maintain weight, cut fat, prep for exam): ").strip()
    cals = input("Target Calories (e.g., 2000): ").strip()
    metrics = f"Goal: {goal}, Target Calories: {cals}"
    
    print("\nGenerating Indian Hostel plan...")
    print("\n" + generate_holistic_plan(metrics))

def main():
    while True:
        c = menu()
        if c == "1": handle_create_tt()
        elif c == "2": handle_review_tt()
        elif c == "3": handle_analyze_tt()
        elif c == "4": handle_tdee()
        elif c == "5": handle_log_health()
        elif c == "6": handle_analyze_log()
        elif c == "7": handle_holistic_plan()
        elif c == "8": 
            print("\nSystem shut down. Stay consistent. 💥")
            break
        else: print("Invalid option.")

if __name__ == "__main__":
    main()
