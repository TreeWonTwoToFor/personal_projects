import os
import datetime
from math import isclose

def days_left() -> int:
    today = datetime.date.today()
    start_of_break = datetime.date(2024,11,22)
    end_of_break = datetime.date(2024,12,2)
    end_of_quarter = datetime.date(2024,12,13)
    diff = end_of_quarter-today-(end_of_break-start_of_break)
    return diff.days

def cost_per_meal(days: int, dollars: int, meals_per_day: float = 0.0) -> None:
    if isclose(meals_per_day, 0.0):
        # user didn't select a value
        meal_number_options = [2.0, 2.25, 2.5, 2.75, 3.0]
        for meal in meal_number_options:
            total_meals = meal * days
            print(f"{meal} meals per day: {dollars/total_meals}")
    else:
        total_meals = meals_per_day * days
        print (dollars/total_meals)

def main() -> None:
    os.system("cls")

    days = days_left()
    print(f"Days left in quarter: {days}")

    dollars = int(input("Total dollars (whole number): "))
    meals_per_day = float(input("Meals per day (0 for unsure): "))
    if meals_per_day == 0.0:
        cost_per_meal(days, dollars)
    else:
        cost_per_meal(days, dollars, meals_per_day)

if __name__ == "__main__":
    main()