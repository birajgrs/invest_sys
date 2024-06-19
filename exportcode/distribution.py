import math
from business.models import BusinessHouseData
from business.models import FinancialData

# Combined functions from logic.py
def get_user_input():
    initial_investment = float(input("Enter the initial investment: "))
    total_investment = float(input("Enter the total investment for constructing full power houses: "))
    discount_rate = float(input("Enter the discount rate (as a decimal, e.g., 0.1 for 10%): "))
    operational_days = int(input("Enter the number of operational days per year: "))
    project_lifetime = int(input("Enter the project lifetime in years: "))

    sectors = []
    sector_names = ["public_sector", "hospital", "railway_sector", "oil_corporation"]
    for sector_name in sector_names:
        other_expenses = float(input(f"Enter the other expenses for {sector_name}: "))
        paid_for_nea = float(input(f"Enter the Paid_for_NEA for {sector_name}: "))
        sectors.append({"name": sector_name, "other_expenses": other_expenses, "paid_for_nea": paid_for_nea})

    return initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors


def calculate_roi(initial_investment, total_expenses, total_income):
    if total_income == 0:
        return float('inf')
    return (initial_investment + total_expenses) / total_income


def calculate_npv(initial_investment, total_income, total_expenses, discount_rate, operational_days, project_lifetime):
    npv = -initial_investment
    try:
        for year in range(1, project_lifetime + 1):
            discounted_cash_flow = (total_income - total_expenses) / operational_days / ((1 + discount_rate) ** year)
            npv += discounted_cash_flow
    except OverflowError:
        npv = float('inf')  # or another appropriate value indicating an error

    return npv


def calculate_profitability_index(initial_investment, total_income, total_expenses, discount_rate, operational_days, project_lifetime):
    present_value_of_cash_flows = sum((total_income - total_expenses) / operational_days / ((1 + discount_rate) ** year) for year in range(1, project_lifetime + 1))
    return present_value_of_cash_flows / initial_investment


def calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit):
    return fixed_costs / (price_per_unit - variable_cost_per_unit)


# Combined functions from distribution.py
def get_sector_data(sectors):
    total_paid_for_nea = sum(sector["paid_for_nea"] for sector in sectors)
    for sector in sectors:
        revenue = sector["paid_for_nea"] - sector["other_expenses"]
        sector["revenue"] = revenue
    return sectors


def adjust_distribution(sectors):
    sectors = get_sector_data(sectors)  # Calculate revenue first
    total_revenue = sum(sector["revenue"] for sector in sectors)

    for sector in sectors:
        sector["adjusted_percentage"] = sector["revenue"] / total_revenue if total_revenue != 0 else 0

    return sectors


def calculate_combined_values(sectors, total_investment, discount_rate, operational_days, project_lifetime):
    combined_daily_income = sum(sector["paid_for_nea"] * sector["adjusted_percentage"] for sector in sectors)
    combined_daily_expenses = sum(
        (sector["other_expenses"] + sector["paid_for_nea"]) * sector["adjusted_percentage"] for sector in sectors)

    roi_time = calculate_roi(total_investment, combined_daily_expenses, combined_daily_income)
    npv = calculate_npv(total_investment, combined_daily_income, combined_daily_expenses, discount_rate,
                        operational_days, project_lifetime)
    profitability_index = calculate_profitability_index(total_investment, combined_daily_income,
                                                        combined_daily_expenses, discount_rate, operational_days,
                                                        project_lifetime)

    return roi_time, npv, profitability_index


def display_sector_info(sectors):
    sorted_sectors = sorted(sectors, key=lambda x: x["revenue"], reverse=True)
    most_revenue_sector = sorted_sectors[0]
    least_revenue_sector = sorted_sectors[-1]

    print("\nSector Revenue and Distribution:")
    for sector in sorted_sectors:
        print(
            f"{sector['name']}: Revenue = {sector['revenue']:.2f}, Adjusted Percentage = {sector['adjusted_percentage'] * 100:.2f}%")

    print(
        f"\nSector with the Most Revenue: {most_revenue_sector['name']} with Revenue = {most_revenue_sector['revenue']:.2f}")
    print(
        f"Sector with the Least Revenue: {least_revenue_sector['name']} with Revenue = {least_revenue_sector['revenue']:.2f}")


def main():
    initial_investment, total_investment, discount_rate, operational_days, project_lifetime, sectors = get_user_input()

    # Adjust distribution
    sectors = adjust_distribution(sectors)

    # Before adjustment
    total_daily_income = sum(sector['paid_for_nea'] for sector in sectors)
    total_daily_expenses = sum(sector['other_expenses'] + sector['paid_for_nea'] for sector in sectors)

    roi_time_before = calculate_roi(initial_investment, total_daily_expenses, total_daily_income)
    npv_before = calculate_npv(initial_investment, total_daily_income, total_daily_expenses, discount_rate,
                               operational_days, project_lifetime)
    profitability_index_before = calculate_profitability_index(initial_investment, total_daily_income,
                                                               total_daily_expenses, discount_rate,
                                                               operational_days, project_lifetime)

    fixed_costs = total_investment
    price_per_unit = total_daily_income / operational_days
    variable_cost_per_unit = total_daily_expenses / operational_days
    break_even_units_before = calculate_break_even_point(fixed_costs, price_per_unit, variable_cost_per_unit)

    print("\nBefore distribution adjustment:")
    print(f"ROI Time: {roi_time_before:.2f} days")
    print(f"NPV: {npv_before:.2f}")
    print(f"Profitability Index: {profitability_index_before:.2f}")
    print(f"Break-Even Point: {break_even_units_before:.2f} units/day")
    print("Sector details before adjustment:")
    for sector in sectors:
        print(
            f"{sector['name']}: Daily Income (Paid_for_NEA) = {sector['paid_for_nea']}, Daily Expenses (other expenses + Paid_for_NEA) = {sector['other_expenses'] + sector['paid_for_nea']}")

    # After adjustment
    roi_time_after, npv_after, profitability_index_after = calculate_combined_values(sectors, total_investment,
                                                                                     discount_rate, operational_days,
                                                                                     project_lifetime)

    total_daily_income_after = sum(sector['paid_for_nea'] * sector['adjusted_percentage'] for sector in sectors)
    total_daily_expenses_after = sum(
        (sector['other_expenses'] + sector['paid_for_nea']) * sector['adjusted_percentage'] for sector in sectors)

    price_per_unit_after = total_daily_income_after / operational_days
    variable_cost_per_unit_after = total_daily_expenses_after / operational_days
    break_even_units_after = calculate_break_even_point(fixed_costs, price_per_unit_after,
                                                        variable_cost_per_unit_after)

    print("\nAfter distribution adjustment:")
    print(f"ROI Time: {roi_time_after:.2f} days")
    print(f"NPV: {npv_after:.2f}")
    print(f"Profitability Index: {profitability_index_after:.2f}")
    print(f"Break-Even Point: {break_even_units_after:.2f} units/day")

    # Display sector info
    display_sector_info(sectors)


if __name__ == "__main__":
    main()
