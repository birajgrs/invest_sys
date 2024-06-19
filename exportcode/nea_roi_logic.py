import numpy as np
from sklearn.linear_model import LinearRegression

def get_user_input():
    initial_investment = float(input("Enter the initial investment: "))
    total_investment = float(input("Enter the total investment for constructing full power houses: "))
    operational_days = int(input("Enter the number of operational days per year: "))
    project_lifetime = int(input("Enter the project lifetime in years: "))
    daily_expenses = float(input("Enter the daily expenses of NEA: "))
    discount_rate = float(input("Enter the daily expenses of NEA: "))

    return initial_investment, total_investment, operational_days, project_lifetime, daily_expenses,discount_rate

def get_sector_data():
    sectors = {
        "public_sector": {"percentage": 0.25, "daily_income": 10000, "daily_expenses": 5000},
        "hospital": {"percentage": 0.25, "daily_income": 15000, "daily_expenses": 7000},
        "railway_sector": {"percentage": 0.25, "daily_income": 20000, "daily_expenses": 8000},
        "oil_corporation": {"percentage": 0.25, "daily_income": 30000, "daily_expenses": 10000},
    }
    return sectors

def update_nea_income(nea_income, sector_data):
    for sector, data in sector_data.items():
        nea_income += data["percentage"] * data["daily_expenses"]
    return nea_income

def calculate_roi_with_linear_regression(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model.predict(X)

def calculate_npv(initial_investment, nea_income, daily_expenses, discount_rate, operational_days, project_lifetime):
    npv = 0
    for t in range(project_lifetime):
        cash_flow = (nea_income - daily_expenses) * operational_days
        npv += cash_flow / (1 + discount_rate) ** (t + 1)
    npv -= initial_investment
    return npv

def calculate_profitability_index(initial_investment, nea_income, daily_expenses, discount_rate, operational_days, project_lifetime):
    pv_cash_flows = 0
    for t in range(project_lifetime):
        cash_flow = (nea_income - daily_expenses) * operational_days
        pv_cash_flows += cash_flow / (1 + discount_rate) ** (t + 1)
    pi = pv_cash_flows / initial_investment
    return pi

def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    break_even_units = fixed_costs / (price_per_unit - variable_cost_per_unit)
    return break_even_units

# Main script
if __name__ == "__main__":
    print("Welcome to the Financial Analysis Tool for NEA (Nepal Electricity Authority)")
    print("Please provide the following details:")
    initial_investment, total_investment, operational_days, project_lifetime, daily_expenses_nea = get_user_input()

    # Get sector data
    sector_data = get_sector_data()

    # Calculate NEA's income
    nea_income = sum(data["percentage"] * data["daily_expenses"] for data in sector_data.values())

    # Predict ROI using linear regression
    X = np.array([[nea_income]])
    y = np.array([[daily_expenses_nea]])
    model = LinearRegression().fit(X, y)
    roi_time_predicted = model.predict(X)[0][0]

    # Calculate financial metrics
    npv = calculate_npv(initial_investment, nea_income, daily_expenses_nea, discount_rate, operational_days, project_lifetime)
    profitability_index = calculate_profitability_index(initial_investment, nea_income, daily_expenses_nea, discount_rate, operational_days, project_lifetime)

    # Calculate break-even point
    fixed_costs = total_investment
    price_per_unit = nea_income / operational_days
    variable_cost_per_unit = daily_expenses_nea / operational_days
    break_even_units = calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)

    print("\nFinancial Analysis Results:")
    print(f"ROI Time (Predicted): {roi_time_predicted:.2f} days")
    print(f"NPV: {npv:.2f}")
    print(f"Profitability Index: {profitability_index:.2f}")
    print(f"Break-Even Point: {break_even_units:.2f} units/day")
