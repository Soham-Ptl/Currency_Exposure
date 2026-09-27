import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
df_exposure = pd.DataFrame()
df2 = pd.read_csv("simulation.csv")

df["Revenue_INR"] = df["Revenue"] * df["Exchange_Rate_INR"]
df["Expenses_INR"] = df["Expenses"] * df["Exchange_Rate_INR"]
print(df.to_string())





print("\n===============================================\n")
print("               Financial Summary :")
print("\n-----------------------------------------------\n")
totalRevenue = df["Revenue_INR"].sum()
totalExpenses = df["Expenses_INR"].sum()
totalProfit = totalRevenue - totalExpenses

print (f"Total Revenue  : {totalRevenue} \nTotal Expenses : {totalExpenses} \nTotal Profit   : {totalProfit}")
print("\n===============================================\n\n\n")





print("\n===============================================\n")
print("               Currency Exposure :")
print("\n-----------------------------------------------\n")

df_exposure["Currency"] = df["Currency"]
df_exposure["Net_Exposure"] = df["Revenue"] - df["Expenses"]
df_exposure["Net_Exposure_INR"] = df_exposure["Net_Exposure"] * df["Exchange_Rate_INR"]
df_exposure["Exposure_%"] = (df_exposure["Net_Exposure_INR"].abs() / df_exposure["Net_Exposure_INR"].abs().sum()) * 100
print(df_exposure.to_string())
print("\n===============================================\n\n\n")





print(df2.to_string())
print("\n\n\n")
result = pd.DataFrame()   
temp = pd.DataFrame() 


for i in range ( len(df2) ):
    scenario = df2.iloc[i]

    changes = {
        "USD": scenario["USD_Change"],
        "GBP": scenario["GBP_Change"],
        "EUR": scenario["EUR_Change"],
        "JPY": scenario["JPY_Change"],
        "AUD": scenario["AUD_Change"]
    }

    temp["Change"] = df["Currency"].map(changes)

    temp["New_Rate"] = (
        df["Exchange_Rate_INR"] * (1 + temp["Change"])
    )

    temp["New_Revenue_INR"] = df["Revenue"] * temp["New_Rate"]
    temp["New_Expenses_INR"] = df["Expenses"] * temp["New_Rate"]
    NewRevenueTotal = temp["New_Revenue_INR"].sum()
    NewExpenseTotal = temp["New_Expenses_INR"].sum()
    NewProfit = NewRevenueTotal - NewExpenseTotal

    result.loc[i, "Scenario"] = scenario["Scenario"]
    result.loc[i, "Total_Revenue_INR"] = NewRevenueTotal
    result.loc[i, "Total_Expenses_INR"] = NewExpenseTotal
    result.loc[i, "Total_Profit_INR"] = NewProfit

base_profit = result.loc[result["Scenario"] == "Base","Total_Profit_INR"].iloc[0]
result["Profit_Change_From_Base"] = (result["Total_Profit_INR"] - base_profit)


print("\n===============================================\n")
print("               Scenario Summary :")
print("\n-----------------------------------------------\n")
print(result.to_string())
print("\n===============================================\n\n\n")





# Plotting profit change from base scenario for each scenario

plt.figure(figsize=(12, 6))

plt.bar(
    result["Scenario"],
    result["Profit_Change_From_Base"]
)

plt.axhline(0, linewidth=1)

plt.xlabel("Scenario")
plt.ylabel("Change in Profit (INR)")
plt.title("Profit Impact Relative to Base Case")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig("plots/profit_impact.png", dpi=300)





# Plotting Sensitivity Based on Net Exposure

plt.figure(figsize=(8, 8))

plt.pie(
    df_exposure["Exposure_%"],
    labels=df_exposure["Currency"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Currency Sensitivity Based on Net Exposure")

plt.tight_layout()

plt.savefig("plots/currency_sensitivity.png", dpi=300)