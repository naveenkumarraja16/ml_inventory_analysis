# # perfect file
import pandas as pd
import matplotlib.pyplot as plt
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
product_sales = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])['Quantity'].sum()

# Calculate the average sales per week for each product in the last four weeks
average_sales_per_week = product_sales / 4

# Predict the sales for each product in the next week
predicted_next_week_sales = average_sales_per_week

# Calculate the predicted overall sales for the next week
predicted_overall_sales_next_week = predicted_next_week_sales.sum()




# In this code, the groupby function is used to group the data by both the 'Organisation Name' and 'Product Name' columns. 
# Then, the agg function is applied to calculate different metrics for each group. Here's a breakdown of the calculations:

# 'Quantity': 'sum': Calculates the total quantity sold for each product in the last four weeks.
# 'cost to company': 'mean': Calculates the average cost to the company for each product.
# 'profit': 'mean': Calculates the average profit for each product.
# 'manpower': 'mean': Calculates the average manpower used for each product.
# 'time': 'mean': Calculates the average time to manufacture each product.
# By applying these calculations, you can obtain a summary of the sales analysis for each product in the last four weeks,
#  including the total quantity sold, average cost, average profit, average manpower, and average manufacturing time.
# Analyze the last four weeks sales based on product information
last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Organisation Name', 'Product Name']).agg({
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







# # Generate bar graphs for each organization and each product, showing sales for each week in the last four weeks
# organizations = last_four_weeks_sales_analysis['Organisation Name'].unique()
# products = last_four_weeks_sales_analysis['Product Name'].unique()

# for org_name in organizations:
#     org_data = last_four_weeks_sales_analysis[last_four_weeks_sales_analysis['Organisation Name'] == org_name]
    
#     for product_name in products:
#         product_data = org_data[org_data['Product Name'] == product_name]
        
#         if not product_data.empty:
#             org_product_data = last_four_weeks_data[(last_four_weeks_data['Organisation Name'] == org_name) &
#                                                     (last_four_weeks_data['Product Name'] == product_name)]
#             product_sales = org_product_data.groupby(org_product_data['Date'].dt.strftime('%Y-%U'))['Quantity'].sum()

#             plt.figure()
#             plt.title(f'Sales for {org_name} - {product_name} - Last Four Weeks')
#             plt.xlabel('Week')
#             plt.ylabel('Quantity Sold')
#             plt.bar(product_sales.index, product_sales.values)
#             plt.xticks(rotation=45)
#             plt.show()

# Predict the sales for each product in the next week and add it to the analysis
next_week_sales_analysis = last_four_weeks_sales_analysis.copy()
next_week_sales_analysis['Predicted Sales Next Week'] = predicted_next_week_sales.values

# Generate bar graphs for each organization and each product, showing sales for each week in the last four weeks
organizations = last_four_weeks_sales_analysis['Organisation Name'].unique()
products = last_four_weeks_sales_analysis['Product Name'].unique()

for org_name in organizations:
    org_data = last_four_weeks_sales_analysis[last_four_weeks_sales_analysis['Organisation Name'] == org_name]

    for product_name in products:
        product_data = org_data[org_data['Product Name'] == product_name]

        if not product_data.empty:
            org_product_data = last_four_weeks_data[(last_four_weeks_data['Organisation Name'] == org_name) &
                                                    (last_four_weeks_data['Product Name'] == product_name)]
            product_sales = org_product_data.groupby(org_product_data['Date'].dt.strftime('%Y-%U'))['Quantity'].sum()

            plt.figure()
            plt.title(f'Sales for {org_name} - {product_name} - Last Four Weeks')
            plt.xlabel('Week')
            plt.ylabel('Quantity Sold')
            plt.bar(product_sales.index, product_sales.values)

            # Add the predicted sales for the next week to the graph
            if org_name in next_week_sales_analysis['Organisation Name'].values and \
                    product_name in next_week_sales_analysis['Product Name'].values:
                predicted_sales = next_week_sales_analysis.loc[
                    (next_week_sales_analysis['Organisation Name'] == org_name) &
                    (next_week_sales_analysis['Product Name'] == product_name),
                    'Predicted Sales Next Week'
                ].values[0]
                plt.bar('Next Week', predicted_sales, color='green', label='Predicted Sales Next Week')

            plt.xticks(rotation=45)
            plt.legend()
            plt.show()

# Calculate the EOQ for each product
next_week_sales_analysis['EOQ'] = ((2 * next_week_sales_analysis['Ordering Cost'] *
                                    next_week_sales_analysis['Predicted Sales Next Week']) /
                                   next_week_sales_analysis['cost to company']) ** 0.5

# Calculate the next week calendar for each product based on available manpower and time to manufacture
next_week_calendar = next_week_sales_analysis.copy()
next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales.values
next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7


# Print the EOQ for each product
print("\nEOQ (Economic Order Quantity) for Each Product:")
print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']])

# Print the predicted overall sales for the next week
print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# Print the predicted sales for the next week
print("\nPredicted Sales for the Next Week:")
print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales Next Week']])


# Print the next week calendar
print("\nNext Week Calendar:")
print(next_week_calendar[['Organisation Name', 'Product Name', 'Quantity to Manufacture', 'Manpower Required', 'Time Required', 'Completion Time']])







# Print the formulas
print("\nFormulas:")
print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
print("Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4")
print("Predicted Sales for Each Product in the Next Week = Average Sales per Week")
print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
print("Completion Time for Each Product in the Next Week = Time Required + 7")
print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / cost to company) ** 0.5")

import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
from datetime import datetime
import os

# Create a dictionary to store the print statements and graphs
print_statements = {
    "Overall Sales for the Last Four Weeks": overall_sales_last_four_weeks,
    "Sales for the Last Four Weeks": last_four_weeks_sales_analysis,
    "Summary for Last Four Weeks": last_four_weeks_summary,
    "EOQ (Economic Order Quantity) for Each Product": next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']],
    "Predicted Overall Sales for the Next Week": predicted_overall_sales_next_week,
    "Predicted Sales for the Next Week": next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales Next Week']],
    "Next Week Calendar": next_week_calendar[['Organisation Name', 'Product Name', 'Quantity to Manufacture', 'Manpower Required', 'Time Required', 'Completion Time']],
    "Formulas": [
        "Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks",
        "Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4",
        "Predicted Sales for Each Product in the Next Week = Average Sales per Week",
        "Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product",
        "Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower",
        "Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time",
        "Completion Time for Each Product in the Next Week = Time Required + 7",
        "EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / cost to company) ** 0.5"
    ]
}

# Create the Excel writer
writer = pd.ExcelWriter(f"./inventory_analysis/calendar_{datetime.now().strftime('%Y-%m-%d')}.xlsx", engine='xlsxwriter')

# Write each print statement to the first sheet in the Excel file
sheet_name = "Print Statements"
start_row = 0

for title, data in print_statements.items():
    if isinstance(data, pd.DataFrame):
        data.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False, header=True)
        start_row += len(data) + 2
    elif isinstance(data, list):
        df = pd.DataFrame(data, columns=[title])
        df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False, header=True)
        start_row += len(df) + 2
    else:
        df = pd.DataFrame({title: [data]})
        df.to_excel(writer, sheet_name=sheet_name, startrow=start_row, index=False, header=True)
        start_row += 3

# Create a new sheet for graphs
graph_sheet_name = "Graphs"
workbook = writer.book
graph_sheet = workbook.add_worksheet(graph_sheet_name)

# Generate and add graphs to the "Graphs" sheet
start_row = 0

# Create a directory to store the graph images
graph_directory = "./inventory_analysis/graphs"
os.makedirs(graph_directory, exist_ok=True)

for title, data in print_statements.items():
    if isinstance(data, pd.DataFrame):
        # Generate the graph
        plt.figure()
        data.plot(kind='bar')
        plt.title(title)

        # Save the graph as a PNG file in the graph directory
        graph_filename = f'{title}_graph.png'
        graph_filepath = os.path.join(graph_directory, graph_filename)
        plt.savefig(graph_filepath, format='png')
        plt.close()

        # Insert the graph into the "Graphs" sheet
        graph_sheet.insert_image(start_row, 0, graph_filepath, {'x_offset': 25, 'y_offset': 10})

        start_row += 20  # Adjust the starting row for the next graph

for org_name in organizations:
    org_data = last_four_weeks_sales_analysis[last_four_weeks_sales_analysis['Organisation Name'] == org_name]

    for product_name in products:
        product_data = org_data[org_data['Product Name'] == product_name]

        if not product_data.empty:
            org_product_data = last_four_weeks_data[(last_four_weeks_data['Organisation Name'] == org_name) &
                                                    (last_four_weeks_data['Product Name'] == product_name)]
            product_sales = org_product_data.groupby(org_product_data['Date'].dt.strftime('%Y-%U'))['Quantity'].sum()

            plt.figure()
            plt.title(f'Sales for {org_name} - {product_name} - Last Four Weeks')
            plt.xlabel('Week')
            plt.ylabel('Quantity Sold')
            plt.bar(product_sales.index, product_sales.values)

            # Add the predicted sales for the next week to the graph
            if org_name in next_week_sales_analysis['Organisation Name'].values and \
                    product_name in next_week_sales_analysis['Product Name'].values:
                predicted_sales = next_week_sales_analysis.loc[
                    (next_week_sales_analysis['Organisation Name'] == org_name) &
                    (next_week_sales_analysis['Product Name'] == product_name),
                    'Predicted Sales Next Week'
                ].values[0]
                plt.bar('Next Week', predicted_sales, color='green', label='Predicted Sales Next Week')

            plt.xticks(rotation=45)
            plt.legend()

            # Save the graph as a PNG file in the graph directory
            graph_filename = f'{org_name}_{product_name}_graph.png'
            graph_filepath = os.path.join(graph_directory, graph_filename)
            plt.savefig(graph_filepath, format='png')
            plt.close()

            # Insert the graph into the "Graphs" sheet
            graph_sheet.insert_image(start_row, 0, graph_filepath, {'x_offset': 25, 'y_offset': 10})

            start_row += 20  # Adjust the starting row for the next graph

# Save the Excel file
writer._save()

print(f"Exported print statements and graphs to Excel file: ./inventory_analysis/calendar_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
