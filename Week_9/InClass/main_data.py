#main_data.py
import pandas as pd
import matplotlib.pyplot as plt # for control of figure size, subplots, and display
import seaborn as sns # data visualization tool

# Load the dataset
df = pd.read_csv('covid_data.csv')
# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Fill missing values if needed
df.fillna(0, inplace=True)


# Set the aesthetic style of the plots
sns.set(style="whitegrid")

# Create a figure for the dashboard
plt.figure(figsize=(14, 10))

# 1. Time series of cases over time

# subplots are smaller plots inside a larger figure (for displaying more than 1 chart)
# ptl.subplot(nrows in grid, ncolumns, index for which subplot position you're currently working on)
plt.subplot(3, 1, 1) # sets up the first subplot in a 3-row, 1-column layout
sns.lineplot(data=df, x='date', y='cases', hue='country', palette='viridis') # draws linechart with differing county colors
plt.title('COVID-19 Cases Over Time by Country')
plt.ylabel('Number of Cases')
plt.xticks(rotation=45) # rotates date labels for readablility

# 2. Time series of deaths over time
plt.subplot(3, 1, 2)
sns.lineplot(data=df, x='date', y='deaths', hue='country', palette='Reds')
plt.title('COVID-19 Deaths Over Time by Country')
plt.ylabel('Number of Deaths')
plt.xticks(rotation=45)

# 3. Vaccination rates over time
plt.subplot(3, 1, 3)
sns.lineplot(data=df, x='date', y='vaccinations', hue='country', palette='Blues')
plt.title('COVID-19 Vaccinations Over Time by Country')
plt.ylabel('Number of Vaccinations')
plt.xticks(rotation=45)

# Show the dashboard
plt.tight_layout() # automatically adjusts spacing between subplots to prevent overlapping labels or titles.
plt.show()
