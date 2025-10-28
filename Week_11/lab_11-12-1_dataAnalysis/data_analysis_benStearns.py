########################################################################################################################
# Title............: Lab 11.12.1 - Data Analysis
# Author...........: Ben Stearns
# Date.............: 10-28-2025
# Purpose..........: The purpose of this program is to:
#######################################################################################################################

# imports
import numpy as np               # for support of arrays and matrices
import pandas as pd              # for dataframe data containment/visualization
import matplotlib.pyplot as plt  # to visualizing data as plot charts
import seaborn as sns            # for enhanced data visualization tools

# retrieve and store seaborn's built-in data set for restaurant tips
tips = sns.load_dataset("tips")

# print the first 5 rows of data
print(tips.head())

# print descriptive statistics for the data
print()
print(tips.describe())

# Total Bill Amounts Histogram - observes most common total bill amounts
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8,6))
sns.histplot(tips['total_bill'], bins=20, kde=True)
plt.title('Distribution of Total Bill Amounts')
plt.xlabel('Total Bill ($)')
plt.ylabel('Frequency')
plt.show()

# Scatterplot of Total Bill vs Tip - analyzes correlation between total bill and how other elements factor in
plt.figure(figsize=(8,6))
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time',style='smoker',size='size')
plt.title('Total Bill vs Tip Amount')
plt.xlabel('Total Bill ($)')
plt.ylabel('Tip ($)')
plt.legend(title='Time of Day / Smoker / Party Size')
plt.show()

# box plot of tips by day - compare median tip amounts across different days and bw genders to identify patterns
plt.figure(figsize=(8,6))
sns.boxplot(data=tips, x='day', y='tip', hue='sex')
plt.title('Tip Amounts by Day and Gender')
plt.xlabel('Day of the Week')
plt.ylabel('Tip ($)')
plt.legend(title='Gender')
plt.show()

# calculate average tip percentage for smokers vs nonsmokers
tips['tip_percent'] = tips['tip'] / tips['total_bill'] * 100
average_tip_smoker = tips.groupby('smoker',observed=True)['tip_percent'].mean()
print('\nAverage Tip Percentage by Smoker Status: ')
print(average_tip_smoker)

# See if large parties tip more on average
average_tip_party_size = tips.groupby('size',observed=True)['tip_percent'].mean()
print('\nAverage Tip Amount by Party Size: ')
print(average_tip_party_size)

# Visualize Average Tips by Party Size as a chart
plt.figure(figsize=(8,6))
sns.barplot(x=average_tip_party_size.index, y=average_tip_party_size.values)
plt.title('Average Tip by Party Size')
plt.xlabel('Party Size')
plt.ylabel('Average Tip ($)')
plt.show()

# calculate average tip by time of day and chart
average_tip_by_time = tips.groupby('time')['tip_percent'].mean()
print('\nAverage Tip Percentage by Time of Day / Smoker / Party Size: ')
print(average_tip_by_time)
plt.figure(figsize=(8,6))
sns.barplot(x=average_tip_by_time.index, y=average_tip_by_time.values)
plt.title('Average Tip % by Time of Day')
plt.xlabel('Time of Day')
plt.ylabel('Average Tip Percentage')
plt.show()

# final dashboard
# Create a 2x2 dashboard layout
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Histogram of total bill
sns.histplot(tips['total_bill'], bins=20, kde=True, ax=axes[0, 0])
axes[0, 0].set_title("Distribution of Total Bill")
axes[0, 0].set_xlabel("Total Bill ($)")
axes[0, 0].set_ylabel("Frequency")

# Plot 2: Scatter plot of Total Bill vs Tip
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time', style='smoker', size='size', ax=axes[0, 1])
axes[0, 1].set_title("Total Bill vs Tip")
axes[0, 1].set_xlabel("Total Bill ($)")
axes[0, 1].set_ylabel("Tip ($)")

# Plot 3: Box plot of Tips by Day and Gender
sns.boxplot(data=tips, x='day', y='tip', hue='sex', ax=axes[1, 0])
axes[1, 0].set_title("Tip by Day and Gender")
axes[1, 0].set_xlabel("Day")
axes[1, 0].set_ylabel("Tip ($)")

# Plot 4: Average Tip Percentage by Time of Day
avg_tip_percent_time = tips.groupby('time', observed=True)['tip_percent'].mean().reset_index()
sns.barplot(data=avg_tip_percent_time, x='time', y='tip_percent', ax=axes[1, 1])
axes[1, 1].set_title("Average Tip % by Time of Day")
axes[1, 1].set_xlabel("Time of Day")
axes[1, 1].set_ylabel("Tip %")

# Layout adjustments
plt.tight_layout()
plt.show()