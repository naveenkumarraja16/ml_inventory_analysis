import pandas as pd
from datetime import datetime, timedelta

# Read the sales data from user input
sales_data = pd.read_csv('./developed_data/createdData.csv')
sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# Read the product data from user input
product_data = pd.read_csv('./developed_data/product_data.csv')

# Merge sales data and product data based on product name
merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# Calculate the date range for the last four weeks
current_date = datetime.now().date()
four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
four_weeks_ago = pd.Timestamp(four_weeks_ago)

# Filter the merged data for the last four weeks
last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# Calculate the overall sales for the last four weeks
overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# Calculate the sales for each product in the last four weeks
product_sales = last_four_weeks_data.groupby('Product Name')['Quantity'].sum()

# Calculate the average sales per day for each product in the last four weeks
average_sales_per_day = product_sales / 28

# Predict the sales for each product in the next week
predicted_next_week_sales = average_sales_per_day * 7

# Calculate the predicted overall sales for the next week
predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# Analyze the last four weeks sales based on product information
last_four_weeks_sales_analysis = last_four_weeks_data.groupby('Product Name').agg({
    'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
    'cost to company': 'mean',  # Average cost to the company for the product
    'profit': 'mean',  # Average profit for the product
    'manpower': 'mean',  # Average manpower used for the product
    'time': 'mean',  # Average time to manufacture the product
}).reset_index()

# Add predicted next week sales to the analysis
last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# Check if "Ordering Cost" column exists in the dataset
if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
    # Use the value from the dataset as the ordering cost
    last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
else:
    # Set a default ordering cost of 100 for all products
    last_four_weeks_sales_analysis['Ordering Cost'] = 100

# Calculate the EOQ (Economic Order Quantity) for each product
last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
                                         last_four_weeks_sales_analysis['Predicted Sales']) /
                                        last_four_weeks_sales_analysis['cost to company']) ** 0.5

# Print the overall sales for the last four weeks
print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# Print the sales for each product in the last four weeks
print("\nSales for the Last Four Weeks:")
print(last_four_weeks_sales_analysis)

# Calculate the summary for the last four weeks sales
last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# Print the summary for the last four weeks sales
print("\nSummary for Last Four Weeks:")
print(last_four_weeks_summary)

# Analyze the next week sales based on product information
next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# Update the "Quantity to Manufacture" column in the next week sales analysis
next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# Calculate the next week calendar for each product based on available manpower and time to manufacture
next_week_calendar = next_week_sales_analysis.copy()
next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# Print the predicted sales for the next week
print("\nPredicted Sales for the Next Week:")
print(next_week_sales_analysis[['Product Name', 'Predicted Sales']])

# Print the predicted overall sales for the next week
print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# Print the EOQ for each product
print("\nEOQ (Economic Order Quantity) for Each Product:")
print(next_week_sales_analysis[['Product Name', 'EOQ']])

# Print the next week calendar
print("\nNext Week Calendar:")
print(next_week_calendar)

# Formulas
print("\nFormulas:")
print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
print("Average Sales per Day for Each Product in the Last Four Weeks = Total quantity sold for each product / 28")
print("Predicted Sales for Each Product in the Next Week = Average Sales per Day * 7")
print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
print("Completion Time for Each Product in the Next Week = Time Required + 7")
print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")
