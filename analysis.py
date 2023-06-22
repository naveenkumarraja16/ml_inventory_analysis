

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
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter
from datetime import datetime

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

            # Save the graph as a PNG file
            graph_filename = f'{org_name}_{product_name}_graph.png'
            plt.savefig(graph_filename, format='png')
            plt.close()

            # Insert the graph into the "Graphs" sheet
            graph_sheet.insert_image(start_row, 0, graph_filename, {'x_offset': 25, 'y_offset': 10})

            start_row += 20  # Adjust the starting row for the next graph
for title, data in print_statements.items():
    if isinstance(data, pd.DataFrame):
        # Generate the graph
        plt.figure()
        data.plot(kind='bar')
        plt.title(title)

        # Add the graph to the worksheet
        worksheet_name = graph_sheet_name if len(title) <= 31 else title[:31]  # Limit worksheet name to 31 characters
        graph_sheet.insert_image(start_row, 0, f'{title}_graph.png', {'x_offset': 25, 'y_offset': 10})
        plt.savefig(f'{title}_graph.png', format='png')
        plt.close()

        start_row += 20  # Adjust the starting row for the next graph


# Save the Excel file
writer._save()

print(f"Exported print statements and graphs to Excel file: ./inventory_analysis/calendar_{datetime.now().strftime('%Y-%m-%d')}.xlsx")
















#  four week graph
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])['Quantity'].sum()

# # Calculate the average sales per week for each product in the last four weeks
# average_sales_per_week = product_sales / 4

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_week

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Organisation Name', 'Product Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Check if "Ordering Cost" column exists in the dataset
# if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
#     # Use the value from the dataset as the ordering cost
#     last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
# else:
#     # Set a default ordering cost of 100 for all products
#     last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # # Generate bar graphs for each organization, showing sales for each product in the last four weeks
# # organizations = last_four_weeks_sales_analysis['Organisation Name'].unique()

# # for org_name in organizations:
# #     org_data = last_four_weeks_sales_analysis[last_four_weeks_sales_analysis['Organisation Name'] == org_name]
# #     products = org_data['Product Name']
# #     weeks = last_four_weeks_data['Date'].dt.strftime('%Y-%U').unique()
    
# #     plt.figure()
# #     plt.title(f'Sales for {org_name} - Last Four Weeks')
# #     plt.xlabel('Week')
# #     plt.ylabel('Quantity Sold')
    
# #     # Plot bar graphs for each product
# #     for product in products:
# #         product_data = last_four_weeks_data[(last_four_weeks_data['Organisation Name'] == org_name) &
# #                                             (last_four_weeks_data['Product Name'] == product)]
# #         product_sales = product_data.groupby(product_data['Date'].dt.strftime('%Y-%U'))['Quantity'].sum()
# #         plt.bar(product_sales.index, product_sales.values, label=product)
    
# #     plt.legend()
# #     plt.xticks(rotation=45)
# #     plt.show()

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



# # Calculate the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Print the formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Week")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / cost to company) ** 0.5")



















# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])['Quantity'].sum()

# # Calculate the average sales per week for each product in the last four weeks
# average_sales_per_week = product_sales / 4

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_week

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Organisation Name', 'Product Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Check if "Ordering Cost" column exists in the dataset
# if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
#     # Use the value from the dataset as the ordering cost
#     last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
# else:
#     # Set a default ordering cost of 100 for all products
#     last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Plot the sales for each product in the last four weeks
# for org, org_group in last_four_weeks_sales_analysis.groupby('Organisation Name'):
#     plt.figure()
#     plt.title(f'Sales for {org} - Last Four Weeks')
#     plt.xlabel('Product')
#     plt.ylabel('Quantity Sold')
#     plt.bar(org_group['Product Name'], org_group['Quantity'])
#     plt.xticks(rotation=45)
#     plt.show()

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Week")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")

# # Generate graphs for each organization and each week
# organizations = last_four_weeks_sales_analysis['Organisation Name'].unique()
# weeks = last_four_weeks_data['Date'].dt.strftime('%Y-%U').unique()

# # Generate sales data for each organization and each week
# organizations = last_four_weeks_sales_analysis['Organisation Name'].unique()
# weeks = last_four_weeks_data['Date'].dt.strftime('%Y-%U').unique()

# for org in organizations:
#     org_data = last_four_weeks_sales_analysis[last_four_weeks_sales_analysis['Organisation Name'] == org]
    
#     for week in weeks:
#         week_data = last_four_weeks_data[(last_four_weeks_data['Date'].dt.strftime('%Y-%U') == week) & 
#                                         (last_four_weeks_data['Organisation Name'] == org)]
#         week_start = week_data['Date'].min().strftime('%Y-%m-%d')
#         week_end = week_data['Date'].max().strftime('%Y-%m-%d')

#         # Print the sales data for each product in the week for the current organization
#         print(f"Sales Quantity for {org} - Week {week_start} - {week_end}:")
#         print(week_data[['Product Name', 'Quantity']])
#         print()





















# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])['Quantity'].sum()

# # Calculate the average sales per week for each product in the last four weeks
# average_sales_per_week = product_sales / 4

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_week

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Organisation Name', 'Product Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Check if "Ordering Cost" column exists in the dataset
# if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
#     # Use the value from the dataset as the ordering cost
#     last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
# else:
#     # Set a default ordering cost of 100 for all products
#     last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Plot the sales for each product in the last four weeks
# for org, org_group in last_four_weeks_sales_analysis.groupby('Organisation Name'):
#     plt.figure()
#     plt.title(f'Sales for {org} - Last Four Weeks')
#     plt.xlabel('Product')
#     plt.ylabel('Quantity Sold')
#     plt.bar(org_group['Product Name'], org_group['Quantity'])
#     plt.xticks(rotation=45)
#     plt.show()

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Week")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")

# # Generate graphs for each week
# weeks = last_four_weeks_data['Date'].dt.strftime('%Y-%U').unique()

# for week in weeks:
#     week_data = last_four_weeks_data[last_four_weeks_data['Date'].dt.strftime('%Y-%U').isin([week])]
#     week_start = week_data['Date'].min().strftime('%Y-%m-%d')
#     week_end = week_data['Date'].max().strftime('%Y-%m-%d')

#     # Plot the sales for each product in the week
#     plt.figure(figsize=(8, 6))
#     plt.bar(week_data['Product Name'], week_data['Quantity'])
#     plt.xlabel('Product')
#     plt.ylabel('Sales Quantity')
#     plt.title(f'Sales Quantity for Week {week_start} - {week_end}')
#     plt.xticks(rotation=45)
#     plt.show()
















# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])['Quantity'].sum()

# # Calculate the average sales per week for each product in the last four weeks
# average_sales_per_week = product_sales / 4

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_week

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Organisation Name', 'Product Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Check if "Ordering Cost" column exists in the dataset
# if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
#     # Use the value from the dataset as the ordering cost
#     last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
# else:
#     # Set a default ordering cost of 100 for all products
#     last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Plot the sales for each product in the last four weeks
# for org, org_group in last_four_weeks_sales_analysis.groupby('Organisation Name'):
#     plt.figure()
#     plt.title(f'Sales for {org} - Last Four Weeks')
#     plt.xlabel('Product')
#     plt.ylabel('Quantity Sold')
#     plt.bar(org_group['Product Name'], org_group['Quantity'])
#     plt.xticks(rotation=45)
#     plt.show()

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Organisation Name', 'Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Week for Each Product in the Last Four Weeks = Total quantity sold for each product / 4")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Week")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")


























# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby('Product Name')['Quantity'].sum()

# # Calculate the average sales per day for each product in the last four weeks
# average_sales_per_day = product_sales / 28

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby('Product Name').agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Check if "Ordering Cost" column exists in the dataset
# if 'Ordering Cost' in last_four_weeks_sales_analysis.columns:
#     # Use the value from the dataset as the ordering cost
#     last_four_weeks_sales_analysis['Ordering Cost'] = last_four_weeks_sales_analysis['Ordering Cost']
# else:
#     # Set a default ordering cost of 100 for all products
#     last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Day for Each Product in the Last Four Weeks = Total quantity sold for each product / 28")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Day * 7")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")


















# # first half
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby('Product Name')['Quantity'].sum()

# # Calculate the average sales per day for each product in the last four weeks
# average_sales_per_day = product_sales / 28

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby('Product Name').agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean',  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Set a default ordering cost of 100 for all products
# last_four_weeks_sales_analysis['Ordering Cost'] = 100

# # Calculate the EOQ (Economic Order Quantity) for each product
# last_four_weeks_sales_analysis['EOQ'] = ((2 * last_four_weeks_sales_analysis['Ordering Cost'] *
#                                          last_four_weeks_sales_analysis['Predicted Sales']) /
#                                         last_four_weeks_sales_analysis['cost to company']) ** 0.5

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks:", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each product based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week:", predicted_overall_sales_next_week)

# # Print the EOQ for each product
# print("\nEOQ (Economic Order Quantity) for Each Product:")
# print(next_week_sales_analysis[['Product Name', 'EOQ']])

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Day for Each Product in the Last Four Weeks = Total quantity sold for each product / 28")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Day * 7")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")
# print("EOQ (Economic Order Quantity) for Each Product = ((2 * Ordering Cost * Predicted Sales) / Cost to Company) ^ 0.5")












# Enhanced First
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the overall sales for the last four weeks
# overall_sales_last_four_weeks = last_four_weeks_data['Quantity'].sum()

# # Calculate the sales for each product in the last four weeks
# product_sales = last_four_weeks_data.groupby('Product Name')['Quantity'].sum()

# # Calculate the average sales per day for each product in the last four weeks
# average_sales_per_day = product_sales / 28

# # Predict the sales for each product in the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Calculate the predicted overall sales for the next week
# predicted_overall_sales_next_week = predicted_next_week_sales.sum()

# # Analyze the last four weeks sales based on product information
# last_four_weeks_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean'  # Average time to manufacture the product
# }).reset_index()

# # Add predicted next week sales to the analysis
# last_four_weeks_sales_analysis['Predicted Sales'] = predicted_next_week_sales.values

# # Print the overall sales for the last four weeks
# print("Overall Sales for the Last Four Weeks: ", overall_sales_last_four_weeks)

# # Print the sales for each product in the last four weeks
# print("\nSales for the Last Four Weeks:")
# print(last_four_weeks_sales_analysis)

# # Calculate the summary for the last four weeks sales
# last_four_weeks_summary = last_four_weeks_sales_analysis.describe()

# # Print the summary for the last four weeks sales
# print("\nSummary for Last Four Weeks:")
# print(last_four_weeks_summary)

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_sales_analysis.copy()

# # Update the "Quantity to Manufacture" column in the next week sales analysis
# next_week_sales_analysis['Quantity to Manufacture'] = predicted_next_week_sales.values

# # Calculate the next week calendar for each organization and their products based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the predicted sales for the next week
# print("\nPredicted Sales for the Next Week:")
# print(next_week_sales_analysis[['Product Name', 'Predicted Sales']])

# # Print the predicted overall sales for the next week
# print("\nPredicted Overall Sales for the Next Week: ", predicted_overall_sales_next_week)

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Formulas
# print("\nFormulas:")
# print("Overall Sales for the Last Four Weeks = Total quantity sold in the last four weeks")
# print("Average Sales per Day for Each Product in the Last Four Weeks = Total quantity sold for each product / 28")
# print("Predicted Sales for Each Product in the Next Week = Average Sales per Day * 7")
# print("Predicted Overall Sales for the Next Week = Sum of Predicted Sales for Each Product")
# print("Manpower Required for Each Product in the Next Week = Quantity to Manufacture * Average Manpower")
# print("Time Required for Each Product in the Next Week = Quantity to Manufacture * Average Time")
# print("Completion Time for Each Product in the Next Week = Time Required + 7")





















# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week based on the average sales per day
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean'  # Average time to manufacture the product
# }).reset_index()

# # Print the results and the analysis of next week sales
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# print("\nNext Week Sales Analysis: ")
# print(next_week_sales_analysis)

# # Calculate the summary
# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("\nSummary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")

# # Add your old prediction of next week sales here based on the last four weeks' data
# previous_predicted_next_week_sales = last_four_weeks_total_sales

# # Calculate the next week calendar for each organization and their products based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales - next_week_calendar['Quantity'].fillna(0)
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Plot the graph of quantity sold per product for the last four weeks
# plt.figure(figsize=(10, 6))
# plt.bar(next_week_sales_analysis['Product Name'], next_week_sales_analysis['Quantity'])
# plt.xlabel('Product Name')
# plt.ylabel('Quantity Sold')
# plt.title('Quantity Sold per Product (Last Four Weeks)')
# plt.xticks(rotation=90)
# plt.show()





















# //////   perfect first half
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week based on the average sales per day
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean'  # Average time to manufacture the product
# }).reset_index()

# # Print the results and the analysis of next week sales
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# print("\nNext Week Sales Analysis: ")
# print(next_week_sales_analysis)

# # Calculate the summary
# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("\nSummary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")

# # Add your old prediction of next week sales here based on the last four weeks' data
# previous_predicted_next_week_sales = last_four_weeks_total_sales

# # Calculate the next week calendar for each organization and their products based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales - next_week_calendar['Quantity'].fillna(0)
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)

# # Create an Excel file for the analysis
# current_date_str = current_date.strftime('%Y-%m-%d')
# filename = f'next_week_sales_analysis_{current_date_str}.xlsx'
# writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# # Write the next week sales analysis to a worksheet
# next_week_sales_analysis.to_excel(writer, sheet_name='Next Week Sales Analysis', index=False)

# # Write the summary to a separate worksheet
# summary.to_excel(writer, sheet_name='Summary')

# # Write the next week calendar to a separate worksheet
# next_week_calendar.to_excel(writer, sheet_name='Next Week Calendar', index=False)

# # Get the workbook and worksheets
# workbook = writer.book
# next_week_sales_sheet = writer.sheets['Next Week Sales Analysis']
# summary_sheet = writer.sheets['Summary']
# calendar_sheet = writer.sheets['Next Week Calendar']

# # Add a chart to visualize the sales analysis
# chart = workbook.add_chart({'type': 'column'})

# # Configure the chart
# chart.set_title({'name': 'Next Week Sales Analysis'})
# chart.set_x_axis({'name': 'Product Name'})
# chart.set_y_axis({'name': 'Quantity Sold'})

# # Define the chart data range
# chart_data = {
#     'categories': ['Next Week Sales Analysis', 1, 0, next_week_sales_analysis.shape[0], 0],
#     'values': ['Next Week Sales Analysis', 1, 1, next_week_sales_analysis.shape[0], 1],
# }

# # Add the chart data to the chart
# chart.add_series(chart_data)

# # Insert the chart into the worksheet
# next_week_sales_sheet.insert_chart('F2', chart)

# # Add the previous prediction of next week sales to the organization and product analysis worksheet
# org_products_sheet = writer.sheets['Next Week Sales Analysis']
# row = next_week_sales_analysis.shape[0] + 2  # Find the last row of the data
# org_products_sheet.write(row + 1, 0, 'Previous Predicted Next Week Sales')
# org_products_sheet.write(row + 1, 1, previous_predicted_next_week_sales)

# # Add the previous prediction of next week sales to the chart sheet
# chart_sheet = writer.sheets['Next Week Sales Analysis']
# chart_row = next_week_sales_analysis.shape[0] + 3  # Find the last row of the data in the chart sheet
# chart_sheet.write(chart_row, 0, 'Previous Predicted Next Week Sales')
# chart_sheet.write(chart_row, 1, previous_predicted_next_week_sales)

# # Add a data series for the previous prediction to the chart
# chart.add_series({
#     'name': 'Previous Predicted Next Week Sales',
#     'categories': f"='Next Week Sales Analysis'!$A${row + 2}",
#     'values': f"='Next Week Sales Analysis'!$B${row + 2}",
#     'fill': {'color': '#00FF00'}  # Choose a color for the previous prediction
# })

# # Close the workbook
# writer._save()














# second half
# # in this first part must ne changed
# # some more work on analysis must be done
# import pandas as pd
# import xlsxwriter

# # Read the sales data and product data from CSV files
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Create an Excel file for the analysis
# current_date_str = pd.Timestamp.now().strftime('%Y-%m-%d')
# file_name = f"./inventory_analysis/calendar_{current_date_str}.xlsx"
# workbook = xlsxwriter.Workbook(file_name)

# # Create a worksheet for the organization and product analysis
# org_products_sheet = workbook.add_worksheet('Org and Product Analysis')

# # Write the headers for the organization and product analysis
# org_products_sheet.write(0, 0, 'Organisation Name')
# org_products_sheet.write(0, 1, 'Product Name')
# org_products_sheet.write(0, 2, 'Total Sales (Last 4 Weeks)')
# org_products_sheet.write(0, 3, 'Average Cost to Company')
# org_products_sheet.write(0, 4, 'Average Profit')
# org_products_sheet.write(0, 5, 'Average Manpower')
# org_products_sheet.write(0, 6, 'Average Time to Manufacture')

# # Group the merged data by organization and product
# grouped_data = merged_data.groupby(['Organisation Name', 'Product Name'])

# # Write the data for the organization and product analysis
# row = 1
# for (org, product), group in grouped_data:
#     total_sales = group['Quantity'].sum()
#     avg_cost = group['cost to company'].mean()
#     avg_profit = group['profit'].mean()
#     avg_manpower = group['manpower'].mean()
#     avg_time = group['time'].mean()

#     org_products_sheet.write(row, 0, org)
#     org_products_sheet.write(row, 1, product)
#     org_products_sheet.write(row, 2, total_sales)
#     org_products_sheet.write(row, 3, avg_cost)
#     org_products_sheet.write(row, 4, avg_profit)
#     org_products_sheet.write(row, 5, avg_manpower)
#     org_products_sheet.write(row, 6, avg_time)

#     row += 1

# # Create a chart sheet for the product analysis chart
# chart_sheet = workbook.add_worksheet('Product Analysis Chart')

# # Write the headers for the product analysis chart
# chart_sheet.write(0, 0, 'Organization Name')
# chart_sheet.write(0, 1, 'Product Name')
# chart_sheet.write(0, 2, 'Total Sales (Last 4 Weeks)')

# # Create a chart for each organization's products
# chart_row = 1
# chart_col = 0

# for org in merged_data['Organisation Name'].unique():
#     org_products = merged_data.loc[merged_data['Organisation Name'] == org, 'Product Name'].unique()

#     for product in org_products:
#         product_sales = merged_data.loc[
#             (merged_data['Organisation Name'] == org) & (merged_data['Product Name'] == product),
#             'Quantity'
#         ].sum()

#         chart_sheet.write(chart_row, chart_col, org)
#         chart_sheet.write(chart_row, chart_col + 1, product)
#         chart_sheet.write(chart_row, chart_col + 2, product_sales)

#         chart_row += 1

#     # Create a chart for the organization's products
#     chart = workbook.add_chart({'type': 'column'})

#     # Add data series to the chart
#     chart.add_series({
#         'categories': ['Product Analysis Chart', chart_row - len(org_products), chart_col + 1, chart_row - 1, chart_col + 1],
#         'values': ['Product Analysis Chart', chart_row - len(org_products), chart_col + 2, chart_row - 1, chart_col + 2],
#         'data_labels': {'value': True},
#         'fill': {'color': '#FF0000'}  # Choose a color for the chart bars
#     })

#     # Set chart title and axis labels
#     chart.set_title({'name': f'{org} Products Sales (Last 4 Weeks)'})
#     chart.set_x_axis({'name': 'Product Name'})
#     chart.set_y_axis({'name': 'Total Sales'})

#     # Insert the chart into the chart sheet
#     chart_sheet.insert_chart(chart_row, chart_col, chart)

#     chart_row += 20

# # Close the workbook
# workbook.close()

# print(f"Analysis saved successfully in the Excel file: {file_name}")


















#  Second half good with charts with different page
# # perfect 1
# # //added calender little updated analysis missing
# import pandas as pd
# from datetime import datetime, timedelta
# import xlsxwriter

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Create an Excel file for the analysis
# current_date_str = datetime.now().strftime('%Y-%m-%d')
# file_name = f"./inventory_analysis/calendar_{current_date_str}.xlsx"
# workbook = xlsxwriter.Workbook(file_name)

# # Create a worksheet for the organization and product analysis
# org_products_sheet = workbook.add_worksheet('Org and Product Analysis')

# # Write the headers for the organization and product analysis
# org_products_sheet.write(0, 0, 'Organisation Name')
# org_products_sheet.write(0, 1, 'Product Name')
# org_products_sheet.write(0, 2, 'Total Sales (Last 4 Weeks)')
# org_products_sheet.write(0, 3, 'Average Cost to Company')
# org_products_sheet.write(0, 4, 'Average Profit')
# org_products_sheet.write(0, 5, 'Average Manpower')
# org_products_sheet.write(0, 6, 'Average Time to Manufacture')
# org_products_sheet.write(0, 7, 'Predicted Next Week Sales')

# # Write the data for the organization and product analysis
# row = 1

# # Group the merged data by organization and product
# grouped_data = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])

# for (org, product), group in grouped_data:
#     total_sales = group['Quantity'].sum()
#     avg_cost = group['cost to company'].mean()
#     avg_profit = group['profit'].mean()
#     avg_manpower = group['manpower'].mean()
#     avg_time = group['time'].mean()

#     org_products_sheet.write(row, 0, org)
#     org_products_sheet.write(row, 1, product)
#     org_products_sheet.write(row, 2, total_sales)
#     org_products_sheet.write(row, 3, avg_cost)
#     org_products_sheet.write(row, 4, avg_profit)
#     org_products_sheet.write(row, 5, avg_manpower)
#     org_products_sheet.write(row, 6, avg_time)
#     org_products_sheet.write(row, 7, predicted_next_week_sales)

#     row += 1

# # Create a chart sheet for the last four weeks sales
# chart_sheet = workbook.add_chartsheet('Last Four Weeks Sales Chart')

# # Create a chart for the last four weeks sales
# chart = workbook.add_chart({'type': 'column'})

# # Add data series to the chart
# chart.add_series({
#     'categories': f"='Org and Product Analysis'!$B$2:$B${row}",
#     'values': f"='Org and Product Analysis'!$C$2:$C${row}",
#     'data_labels': {'value': True},
#     'fill': {'color': '#FF0000'}  # Choose a color for the chart bars
# })

# # Set chart title and axis labels
# chart.set_title({'name': 'Last Four Weeks Sales'})
# chart.set_x_axis({'name': 'Product Name'})
# chart.set_y_axis({'name': 'Total Sales'})

# # Insert the chart into the chart sheet
# chart_sheet.set_chart(chart)

# # Group the merged data by organization
# grouped_data = last_four_weeks_data.groupby('Organisation Name')

# for org, group in grouped_data:
#     # Create a worksheet for the organization
#     org_sheet_name = f'{org} Analysis'
#     org_sheet = workbook.add_worksheet(org_sheet_name)

#     # Write the headers for the organization analysis
#     org_sheet.write(0, 0, 'Product Name')
#     org_sheet.write(0, 1, 'Total Sales (Last 4 Weeks)')

#     # Write the data for the organization analysis
#     org_row = 1

#     # Group the organization data by product
#     product_grouped_data = group.groupby('Product Name')

#     for product, product_group in product_grouped_data:
#         product_sales = product_group['Quantity'].sum()

#         org_sheet.write(org_row, 0, product)
#         org_sheet.write(org_row, 1, product_sales)

#         org_row += 1

#     # Create a chart for the organization analysis
#     org_chart = workbook.add_chart({'type': 'column'})

#     # Add data series to the chart
#     org_chart.add_series({
#         'categories': f"='{org_sheet_name}'!$A$2:$A${org_row}",
#         'values': f"='{org_sheet_name}'!$B$2:$B${org_row}",
#         'data_labels': {'value': True},
#         'fill': {'color': '#00FF00'}  # Choose a color for the chart bars
#     })

#     # Set chart title and axis labels
#     org_chart.set_title({'name': f'{org} Sales (Last 4 Weeks)'})
#     org_chart.set_x_axis({'name': 'Product Name'})
#     org_chart.set_y_axis({'name': 'Total Sales'})

#     # Insert the chart into the organization worksheet
#     org_sheet.insert_chart('D2', org_chart)

# # Close the workbook
# workbook.close()

# print(f"Analysis saved successfully in the Excel file: {file_name}")


















# # missing next week predicion but good
# not required
# import pandas as pd
# from datetime import datetime, timedelta
# import xlsxwriter

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Create an Excel file for the analysis
# current_date_str = datetime.now().strftime('%Y-%m-%d')
# file_name = f"./inventory_analysis/calendar_{current_date_str}.xlsx"
# workbook = xlsxwriter.Workbook(file_name)

# # Create a worksheet for the organization and product analysis
# org_products_sheet = workbook.add_worksheet('Org and Product Analysis')

# # Write the headers for the organization and product analysis
# org_products_sheet.write(0, 0, 'Organisation Name')
# org_products_sheet.write(0, 1, 'Product Name')
# org_products_sheet.write(0, 2, 'Total Sales (Last 4 Weeks)')
# org_products_sheet.write(0, 3, 'Average Cost to Company')
# org_products_sheet.write(0, 4, 'Average Profit')
# org_products_sheet.write(0, 5, 'Average Manpower')
# org_products_sheet.write(0, 6, 'Average Time to Manufacture')

# # Write the data for the organization and product analysis
# row = 1

# # Group the merged data by organization and product
# grouped_data = last_four_weeks_data.groupby(['Organisation Name', 'Product Name'])

# for (org, product), group in grouped_data:
#     total_sales = group['Quantity'].sum()
#     avg_cost = group['cost to company'].mean()
#     avg_profit = group['profit'].mean()
#     avg_manpower = group['manpower'].mean()
#     avg_time = group['time'].mean()

#     org_products_sheet.write(row, 0, org)
#     org_products_sheet.write(row, 1, product)
#     org_products_sheet.write(row, 2, total_sales)
#     org_products_sheet.write(row, 3, avg_cost)
#     org_products_sheet.write(row, 4, avg_profit)
#     org_products_sheet.write(row, 5, avg_manpower)
#     org_products_sheet.write(row, 6, avg_time)

#     row += 1

# # Create a chart sheet for the product analysis chart
# chart_sheet = workbook.add_worksheet('Product Analysis Chart')

# # Create a chart for each organization's products
# chart_row = 0

# for org in merged_data['Organisation Name'].unique():
#     org_sheet_name = f'{org} Products'
#     org_products = merged_data.loc[merged_data['Organisation Name'] == org, 'Product Name'].unique()

#     # Create a worksheet for the organization's products
#     org_products_sheet = workbook.add_worksheet(org_sheet_name)

#     # Write the headers for the organization's products
#     org_products_sheet.write(0, 0, 'Product Name')
#     org_products_sheet.write(0, 1, 'Total Sales (Last 4 Weeks)')

#     # Write the data for the organization's products
#     org_row = 1

#     for product in org_products:
#         product_sales = last_four_weeks_data.loc[
#             (last_four_weeks_data['Organisation Name'] == org) & (last_four_weeks_data['Product Name'] == product),
#             'Quantity'
#         ].sum()

#         org_products_sheet.write(org_row, 0, product)
#         org_products_sheet.write(org_row, 1, product_sales)

#         org_row += 1

#     # Create a chart for the organization's products
#     chart = workbook.add_chart({'type': 'column'})

#     # Add data series to the chart
#     chart.add_series({
#         'categories': f"='{org_sheet_name}'!$A$2:$A${org_row}",
#         'values': f"='{org_sheet_name}'!$B$2:$B${org_row}",
#         'data_labels': {'value': True},
#         'fill': {'color': '#FF0000'}  # Choose a color for the chart bars
#     })

#     # Set chart title and axis labels
#     chart.set_title({'name': f'{org} Products Sales (Last 4 Weeks)'})
#     chart.set_x_axis({'name': 'Product Name'})
#     chart.set_y_axis({'name': 'Total Sales'})

#     # Insert the chart into the chart sheet
#     chart_sheet.insert_chart(chart_row, 0, chart)

#     # Add the prediction for the next week to the organization's products sheet
#     org_products_sheet.write(org_row + 1, 0, 'Predicted Next Week Sales')
#     org_products_sheet.write(org_row + 1, 1, predicted_next_week_sales)

#     # Add the prediction to the chart worksheet
#     chart_sheet.write(chart_row, 0, 'Predicted Next Week Sales')
#     chart_sheet.write(chart_row, 1, predicted_next_week_sales)

#     # Add a data series for the prediction to the chart
#     chart.add_series({
#         'name': 'Predicted Next Week Sales',
#         'categories': f"='{org_sheet_name}'!$A${org_row + 2}",
#         'values': f"='{org_sheet_name}'!$B${org_row + 2}",
#         'fill': {'color': '#00FF00'}  # Choose a color for the prediction
#     })

#     chart_row += 20

# # Close the workbook
# workbook.close()

# print("Analysis saved successfully in the Excel file.")




















# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean'  # Average time to manufacture the product
# }).reset_index()

# # Calculate the summary
# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("Summary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")

# # Calculate the next week calendar for each organization and their products based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales - next_week_calendar['Quantity'].fillna(0)
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Group the next week calendar by Organisation Name
# grouped_next_week_calendar = next_week_calendar.groupby('Organisation Name')

# # Print the prediction for each organization
# print("\nNext Week Sales Predictions:")
# for org_name, org_group in grouped_next_week_calendar:
#     print("\nOrganization Name:", org_name)
#     print(org_group[['Product Name', 'Quantity to Manufacture', 'Manpower Required', 'Time Required', 'Completion Time']])















# updated with time also
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean',  # Average manpower used for the product
#     'time': 'mean'  # Average time to manufacture the product
# }).reset_index()

# # Print the results and the analysis of next week sales
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# print("\nNext Week Sales Analysis: ")
# print(next_week_sales_analysis)

# # Calculate the summary
# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("\nSummary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")

# # Calculate the next week calendar for each organization and their products based on available manpower and time to manufacture
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales - next_week_calendar['Quantity'].fillna(0)
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']
# next_week_calendar['Time Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['time']
# next_week_calendar['Completion Time'] = next_week_calendar['Time Required'] + 7

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)



























# updated with all manpower and calender

# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',  # Total quantity sold for the product in the last four weeks
#     'cost to company': 'mean',  # Average cost to the company for the product
#     'profit': 'mean',  # Average profit for the product
#     'manpower': 'mean'  # Average manpower used for the product
# }).reset_index()

# # Print the results and the analysis of next week sales
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# print("\nNext Week Sales Analysis: ")
# print(next_week_sales_analysis)

# # Calculate the summary
# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("\nSummary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")

# # Calculate the next week calendar for each organization and their products based on available manpower
# next_week_calendar = next_week_sales_analysis.copy()
# next_week_calendar['Quantity to Manufacture'] = predicted_next_week_sales - next_week_calendar['Quantity'].fillna(0)
# next_week_calendar['Manpower Required'] = next_week_calendar['Quantity to Manufacture'] * next_week_calendar['manpower']

# # Print the next week calendar
# print("\nNext Week Calendar:")
# print(next_week_calendar)














# code with next week prediction

# # In this code, each column in the next_week_sales_analysis DataFrame is described with a comment next to it, explaining how it is calculated. The descriptions are as follows:

# # Quantity: Total quantity sold for the product in the last four weeks.
# # Cost to Company: Average cost to the company for the product.
# # Profit: Average profit for the product.
# # Manpower: Average manpower used for the product.
# # The formulas for calculating the average sales per day in the last four weeks and the predicted sales for the next week are also included as comments at the end of the code for reference.
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# # sales_data_file = input("Enter the file path for the sales data: ")
# sales_data = pd.read_csv('./developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Read the product data from user input
# # product_data_file = input("Enter the file path for the product data: ")
# product_data = pd.read_csv('./developed_data/product_data.csv')

# # Merge sales data and product data based on product name
# merged_data = pd.merge(sales_data, product_data, on='Product Name', how='left')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the merged data for the last four weeks
# last_four_weeks_data = merged_data[merged_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_data['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Analyze the next week sales based on product information
# next_week_sales_analysis = last_four_weeks_data.groupby(['Product Name', 'Organisation Name']).agg({
#     'Quantity': 'sum',
#     'cost to company': 'mean',
#     'profit': 'mean',
#     'manpower': 'mean'
# }).reset_index()

# # Print the results and the analysis of next week sales
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# print("\nNext Week Sales Analysis: ")
# print(next_week_sales_analysis)

# summary = next_week_sales_analysis.describe()

# # Print the summary
# print("\nSummary:")
# print(summary)

# # Formulas
# print("\nFormulas:")
# print("Average Sales per Day in the Last Four Weeks = Total Sales / 28")
# print("Predicted Sales for the Next Week = Average Sales per Day * 7")
























#predict average sales of per day


# import pandas as pd
# from datetime import datetime, timedelta

# # Read the sales data from user input
# sales_data = pd.read_csv('developed_data/createdData.csv')
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Calculate the date range for the last four weeks
# current_date = datetime.now().date()
# four_weeks_ago = (current_date - timedelta(weeks=4)).strftime('%Y-%m-%d')
# four_weeks_ago = pd.Timestamp(four_weeks_ago)

# # Filter the sales data for the last four weeks
# last_four_weeks_sales = sales_data[sales_data['Date'] >= four_weeks_ago]

# # Calculate the sales for the last four weeks
# last_four_weeks_total_sales = last_four_weeks_sales['Quantity'].sum()

# # Calculate the average sales per day in the last four weeks
# average_sales_per_day = last_four_weeks_total_sales / 28

# # Predict the sales for the next week
# predicted_next_week_sales = average_sales_per_day * 7

# # Print the results and the formula used
# print("Sales for the Last Four Weeks: ", last_four_weeks_total_sales)
# print("Predicted Sales for the Next Week: ", predicted_next_week_sales)

# # Print the formula used for predicting next week's sales
# print("Formula Used for Prediction: ")
# print("Predicted Next Week Sales = Average Sales per Day * 7")
# print("Average Sales per Day = Total Sales for Last Four Weeks / 28")







#
#  import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import date, timedelta
# import math
# import os

# # Step 1: Data Collection
# sales_data = pd.read_csv('developed_data/createdData.csv', parse_dates=['Date'])
# product_data = pd.read_csv('developed_data/product_data.csv')

# # Step 2: Analyze Weekly Sales Data
# sales_data = sales_data.groupby(['Date', 'Product Name'])['Quantity'].sum().reset_index()

# # Convert 'Date' column to datetime type with correct format
# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')

# # Extract week number from the 'Date' column
# sales_data['Week'] = sales_data['Date'].dt.isocalendar().week
# weekly_sales = sales_data.groupby(['Product Name', 'Week', 'Date'])['Quantity'].sum().reset_index()

# # Step 4: Calculate Demand and EOQ
# demand_per_week = weekly_sales.groupby(['Product Name', 'Week'])['Quantity'].sum().reset_index()
# demand_per_week = demand_per_week.rename(columns={'Quantity': 'Demand'})
# demand_per_week['EOQ'] = demand_per_week.apply(lambda row: round(math.sqrt((2 * 500 * row['Demand']) / 100), 2), axis=1)

# # Step 5: Export Demand and EOQ to Excel
# excel_folder = 'inventory_analysis'
# os.makedirs(excel_folder, exist_ok=True)
# excel_filename = f"{excel_folder}/inventory_analysis_{date.today().strftime('%Y-%m-%d')}.xlsx"
# excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
# demand_per_week.to_excel(excel_writer, sheet_name='Demand and EOQ', index=False)

# # Step 6: Create Line Plots for Each Product and Save them as Images
# os.makedirs('line_plots', exist_ok=True)

# for product in weekly_sales['Product Name'].unique():
#     product_sales = weekly_sales[weekly_sales['Product Name'] == product]

#     dates = product_sales['Date']
#     quantities = product_sales['Quantity']

#     plt.figure()
#     plt.plot(dates, quantities, marker='o')
#     plt.title(f'Sales Data for {product}')
#     plt.xlabel('Date')
#     plt.ylabel('Quantity Sold')
#     plt.xticks(rotation=45)

#     image_filename = f"line_plots/{product}_line_plot.png"
#     plt.savefig(image_filename)
#     plt.close()

#     worksheet_name = f"{product} Line Plot"
#     worksheet = excel_writer.book.add_worksheet(worksheet_name)
#     worksheet.insert_image('A1', image_filename)

# # Step 7: Create a Pie Chart for Total Sales Distribution and Save it as an Image
# total_sales = weekly_sales.groupby('Product Name')['Quantity'].sum().reset_index()
# product_sales_total = total_sales.groupby('Product Name')['Quantity'].sum()
# plt.figure()
# plt.pie(product_sales_total, labels=product_sales_total.index, autopct='%1.1f%%')
# plt.title("Total Sales Distribution")

# pie_chart_filename = "total_sales_pie_chart.png"
# plt.savefig(pie_chart_filename)
# plt.close()

# worksheet_name = "Total Sales Pie Chart"
# worksheet = excel_writer.book.add_worksheet(worksheet_name)
# worksheet.insert_image('A1', pie_chart_filename)

# # Step 8: Create a Line Plot for Demand and EOQ
# demand_eoq_plot = demand_per_week.groupby('Week')[['Demand', 'EOQ']].sum().reset_index()
# plt.figure()
# plt.plot(demand_eoq_plot['Week'], demand_eoq_plot['Demand'], label='Demand', marker='o')
# plt.plot(demand_eoq_plot['Week'], demand_eoq_plot['EOQ'], label='EOQ', marker='o')
# plt.title("Demand vs. EOQ")
# plt.xlabel("Week")
# plt.ylabel("Quantity")
# plt.legend()

# demand_eoq_plot_filename = "demand_eoq_plot.png"
# plt.savefig(demand_eoq_plot_filename)
# plt.close()

# worksheet_name = "Demand vs. EOQ Plot"
# worksheet = excel_writer.book.add_worksheet(worksheet_name)
# worksheet.insert_image('A1', demand_eoq_plot_filename)

# # Step 9: Save and Close the Excel File
# excel_writer._save()
# excel_writer.close()

# print(f"Exported demand analysis, line plots, charts, and EOQ graph to {excel_filename}")

# # ******************************************************************
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the product data from CSV
# product_data = pd.read_csv('developed_data/product_data.csv')

# # Read the sales data from CSV
# sales_data = pd.read_csv('developed_data/createdData.csv')

# sales_data['Date'] = pd.to_datetime(sales_data['Date'], format='%d-%m-%Y')


# # Extract week number from the 'Date' column
# sales_data['Week'] = sales_data['Date'].dt.isocalendar().week

# # Get the next week's start and end dates
# next_week_start = datetime.today().date() + timedelta(days=7)
# next_week_end = next_week_start + timedelta(days=6)

# # Filter the sales data for the next week
# next_week_sales = sales_data[(sales_data['Date'].dt.date >= next_week_start) &
#                              (sales_data['Date'].dt.date <= next_week_end)]

# # Iterate over each product in the product data
# next_week_calendar = pd.DataFrame(columns=['Product Name', 'Organisation Name', 'Available Quantity', 'Status', 'Quantity Sold'])
# for index, product_row in product_data.iterrows():
#     product_name = product_row['Product Name']
#     org_name = product_row['Organisation Name']

#     # Filter sales data for the product in the next week
#     product_sales = next_week_sales[next_week_sales['Product Name'] == product_name]

#     # Calculate available quantity
#     quantity_sold = product_sales.shape[0]  # Count the number of rows (sales) for the product
#     available_quantity = quantity_sold

#     # Determine the status based on available quantity
#     if available_quantity < 0:
#         status = "Increase production (" + str(abs(available_quantity)) + " products more needed)"
#     elif available_quantity == 0:
#         status = "No action needed"
#     else:
#         status = "Excess inventory (" + str(available_quantity) + " products remaining)"

#     next_week_calendar = next_week_calendar._append({
#         'Product Name': product_name,
#         'Organisation Name': org_name,
#         'Available Quantity': available_quantity,
#         'Status': status,
#         'Quantity Sold': quantity_sold
#     }, ignore_index=True)

# # Print and export the next week calendar
# print(next_week_calendar)
# next_week_calendar.to_excel('inventory_analysis/next_week_calendar_' + str(next_week_start) + '.xlsx', index=False)































# import datetime
# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# from datetime import date, timedelta
# import math
# import os
# import pandas as pd
# import datetime
# from datetime import timedelta


# # Step 1: Data Collection
# # sales_data = pd.read_csv('example_data/sales_data.csv')
# sales_data = pd.read_csv('example_data/sales_data.csv', parse_dates=['Date'])
# product_data = pd.read_csv('example_data/product_data.csv')
# print(product_data)


# # In this step, we start by reading the sales data from a CSV file using the Pandas library.
# # Step 2: Analyze Weekly Sales Data
# sales_data['Date'] = pd.to_datetime(sales_data['Date'])
# sales_data = sales_data.groupby(['Date', 'Product Name'])['Quantity'].sum().reset_index()


# # Here, we convert the 'Date' column to a datetime format and group the data by 
# # 'Date' and 'Product Name', aggregating the 'Quantity' column to get the total sales quantity for each product on each date.
# # Step 3: Analyze Weekly Sales Data
# sales_data['Week'] = sales_data['Date'].dt.isocalendar().week
# weekly_sales = sales_data.groupby(['Product Name', 'Week', 'Date'])['Quantity'].sum().reset_index()


# # Next, we extract the week number from the 'Date' column and add it as a new 'Week' column. 
# # We then group the data by 'Product Name', 'Week', and 'Date', and calculate the total sales quantity for each product in each week.
# # Step 4: Calculate Demand and EOQ
# demand_per_week = weekly_sales.groupby(['Product Name', 'Week'])['Quantity'].sum().reset_index()
# demand_per_week = demand_per_week.rename(columns={'Quantity': 'Demand'})

# # Calculate EOQ for each row
# demand_per_week['EOQ'] = demand_per_week.apply(lambda row: round(math.sqrt((2 * 500 * row['Demand']) / 100), 2), axis=1)  # Assuming carrying cost is $500 and ordering cost is $100


# # In this step, we calculate the demand per week by summing the weekly sales quantity for each product. We rename the 'Quantity' column to 'Demand' for clarity. 
# # Then, we calculate the Economic Order Quantity (EOQ) for each row using the EOQ formula and assuming carrying cost as $500 and ordering cost as $100.
# # Step 5: Export Demand and EOQ to Excel
# excel_folder = 'inventory_analysis'
# os.makedirs(excel_folder, exist_ok=True)  # Create the inventory_analysis directory
# excel_filename = f"{excel_folder}/inventory_analysis_{date.today().strftime('%Y-%m-%d')}.xlsx"
# excel_writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
# demand_per_week.to_excel(excel_writer, sheet_name='Demand and EOQ', index=False)


# # Here, we create a folder to store the inventory analysis and define the filename for the Excel file.
# #  We then create an Excel writer object and save the demand and EOQ data to a new worksheet named 'Demand and EOQ'.
# # Step 6: Create Line Plots for Each Product and Save them as Images
# os.makedirs('line_plots', exist_ok=True)  # Create the line_plots directory

# for product in weekly_sales['Product Name'].unique():
#     product_sales = weekly_sales[weekly_sales['Product Name'] == product]

#     # Prepare data for plotting
#     dates = product_sales['Date']
#     quantities = product_sales['Quantity']

#     # Create a line plot for the sales data
#     plt.figure()
#     plt.plot(dates, quantities, marker='o')
#     plt.title(f'Sales Data for {product}')
#     plt.xlabel('Date')
#     plt.ylabel('Quantity Sold')
#     plt.xticks(rotation=45)

#     # Save the line plot as an image
#     image_filename = f"line_plots/{product}_line_plot.png"
#     plt.savefig(image_filename)
#     plt.close()

#     # Add the line plot image to the Excel file
#     worksheet_name = f"{product} Line Plot"
#     worksheet = excel_writer.book.add_worksheet(worksheet_name)
#     worksheet.insert_image('A1', image_filename)



# # In this step, we iterate over each unique product in the weekly sales data. For each product, we filter the data and extract the dates and quantities. 
# # Then, we create a line plot of the sales data, customize the plot, save it as an image, and close the plot. Finally, we add the line plot image to the Excel file as a new worksheet.
# # Step 7: Create a Pie Chart for Total Sales Distribution and Save it as an Image
# total_sales = weekly_sales.groupby('Product Name')['Quantity'].sum().reset_index()
# product_sales_total = total_sales.groupby('Product Name')['Quantity'].sum()
# plt.figure()
# plt.pie(product_sales_total, labels=product_sales_total.index, autopct='%1.1f%%')
# plt.title("Total Sales Distribution")

# # Save the pie chart as an image
# pie_chart_filename = "total_sales_pie_chart.png"
# plt.savefig(pie_chart_filename)
# plt.close()

# # Add the pie chart image to the Excel file
# worksheet_name = "Total Sales Pie Chart"
# worksheet = excel_writer.book.add_worksheet(worksheet_name)
# worksheet.insert_image('A1', pie_chart_filename)



# # In this step, we calculate the total sales quantity for each product and create a pie chart to visualize the distribution of total sales.
# #  We save the pie chart as an image, close the plot, and add the image to the Excel file as a new worksheet.
# # Step 8: Create a Line Plot for Demand and EOQ
# demand_eoq_plot = demand_per_week.groupby('Week')[['Demand', 'EOQ']].sum().reset_index()
# plt.figure()
# plt.plot(demand_eoq_plot['Week'], demand_eoq_plot['Demand'], label='Demand', marker='o')
# plt.plot(demand_eoq_plot['Week'], demand_eoq_plot['EOQ'], label='EOQ', marker='o')
# plt.title("Demand vs. EOQ")
# plt.xlabel("Week")
# plt.ylabel("Quantity")
# plt.legend()

# # Save the line plot as an image
# demand_eoq_plot_filename = "demand_eoq_plot.png"
# plt.savefig(demand_eoq_plot_filename)
# plt.close()

# # Add the demand vs. EOQ line plot image to the Excel file
# worksheet_name = "Demand vs. EOQ Plot"
# worksheet = excel_writer.book.add_worksheet(worksheet_name)
# worksheet.insert_image('A1', demand_eoq_plot_filename)



# # This step involves creating a line plot to compare the demand and EOQ values over the weeks. 
# # We group the demand and EOQ data by week, plot the lines, add labels and titles, and save the plot as an image. 
# # The image is then added to the Excel file as a new worksheet.
# # Step 9: Save and Close the Excel File
# excel_writer._save()
# excel_writer.close()

# print(f"Exported demand analysis, line plots, charts, and EOQ graph to {excel_filename}")



# # ********************************************************************************
# import pandas as pd
# from datetime import datetime, timedelta

# # Read the dataset from CSV
# dataset = pd.read_csv('example_data/product_data.csv')

# # Get the next week's start and end dates
# next_week_start = datetime.today().date() + timedelta(days=7)
# next_week_end = next_week_start + timedelta(days=6)

# # Filter the sales data for the next week
# next_week_sales = sales_data[(pd.to_datetime(sales_data['Date']).dt.date >= next_week_start) &
#                              (pd.to_datetime(sales_data['Date']).dt.date <= next_week_end)]

# # Iterate over each organization and their products
# next_week_calendar = pd.DataFrame(columns=['Product Name', 'Organisation Name', 'Demand', 'Status', 'Quantity'])
# for index, row in dataset.iterrows():
#     org_products = next_week_sales[next_week_sales['Product Name'] == row['Product Name']]
#     total_demand = org_products['Quantity'].sum()
#     status = ""
#     if total_demand < row['Demand']:
#         status = "Wait for dead product completion (" + str(row['Demand'] - total_demand) + ")"
#     elif total_demand > row['Demand']:
#         status = "Increase production (" + str(total_demand - row['Demand']) + ")"
#     else:
#         status = "No action needed"

#     next_week_calendar = next_week_calendar.append({
#         'Product Name': row['Product Name'],
#         'Organisation Name': row['Organisation Name'],
#         'Demand': row['Demand'],
#         'Status': status,
#         'Quantity': total_demand
#     }, ignore_index=True)

# # Print and export the next week calendar
# print(next_week_calendar)
# next_week_calendar.to_excel('inventory_analysis/next_week_calendar_' + str(next_week_start) + '.xlsx', index=False)
