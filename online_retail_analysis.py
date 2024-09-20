# Online Retail Data Analysis Project

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Step 1: Load the dataset
# Replace the path with your dataset location
df = pd.read_excel(r'C:\path\to\Online Retail.xlsx', index_col=0)

# Display the first few rows to understand the data
df.head()

# Step 2: Data Cleaning

# Check for missing values
print(df.isnull().sum())

# Fill missing values with 0
df.fillna(0, inplace=True)

# Verify that no missing values remain
print(df.isnull().sum())

# Step 3: Handling negative values
# Identify rows with negative UnitPrice
negative_unitprice = df[df['UnitPrice'] < 0][['UnitPrice']]
print("Negative UnitPrice:\n", negative_unitprice)

# Convert negative UnitPrice to 0
df.loc[df['UnitPrice'] < 0, 'UnitPrice'] = 0

# Identify rows with negative Quantity
negative_quantity = df[df['Quantity'] < 0][['Quantity']]
print("Negative Quantity:\n", negative_quantity)

# Convert negative Quantity to 0
df.loc[df['Quantity'] < 0, 'Quantity'] = 0

# Step 4: Remove Duplicates
# Check for duplicated rows
print("Number of duplicated rows:", df.duplicated().sum())

# Step 5: Outlier Detection - Z-Score for Quantity
z_score = np.abs((df['Quantity'] - df['Quantity'].mean()) / df['Quantity'].std())
outliers = df[z_score > 2]
print("Outliers based on Z-Score:\n", outliers[['Quantity', 'InvoiceDate']])

# Visualize Quantity outliers using a box plot
plt.figure(figsize=(8,6))
plt.boxplot(df['Quantity'], vert=False, patch_artist=True)
plt.title('Quantity Outliers')
plt.xlabel('Quantity')
plt.show()

# Step 6: Outlier Detection - Z-Score for UnitPrice
z_score1 = np.abs((df['UnitPrice'] - df['UnitPrice'].mean()) / df['UnitPrice'].std())
outliers1 = df[z_score1 > 2]
print("Outliers based on UnitPrice Z-Score:\n", outliers1[['UnitPrice', 'InvoiceDate']])

# Visualize UnitPrice outliers using a box plot
plt.figure(figsize=(8,6))
plt.boxplot(df['UnitPrice'], vert=False, patch_artist=True)
plt.title('UnitPrice Outliers')
plt.xlabel('UnitPrice')
plt.show()

# Step 7: Data Visualization
# Create a new column for the month of each transaction
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Month'] = df['InvoiceDate'].dt.month

# Group by month and sum the quantities sold
monthly_quantity = df.groupby('Month')['Quantity'].sum().reset_index()
print(monthly_quantity)

# Plot the total quantity sold per month
plt.figure(figsize=(10,6))
plt.bar(monthly_quantity['Month'], monthly_quantity['Quantity'], color='blue')
plt.xlabel('Month')
plt.ylabel('Quantity Sold')
plt.title('Total Quantity Sold per Month')
plt.grid(axis='y')
plt.show()

# Create a new column for the day of the week
df['Day of Week'] = df['InvoiceDate'].dt.day_name()

# Group by day of the week and sum the quantities sold
day_quantity = df.groupby('Day of Week')['Quantity'].sum().reset_index()
print(day_quantity)

# Plot the total quantity sold per day of the week
plt.figure(figsize=(10,6))
plt.bar(day_quantity['Day of Week'], day_quantity['Quantity'], color='red')
plt.xlabel('Day of Week')
plt.ylabel('Quantity Sold')
plt.title('Total Quantity Sold by Day of the Week')
plt.grid(axis='y')
plt.show()
