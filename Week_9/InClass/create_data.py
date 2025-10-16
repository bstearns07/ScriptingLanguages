#create_data.py
import pandas as pd # for data analysis and manipulation (organizing, filtering, cleaning, displaying)
import numpy as np # for numerical computing (algebra, stats, random #'s), especially fast ops on arrays and matrices

# Create a sample dataset
dates = pd.date_range(start="2020-01-01", end="2023-12-31", freq='ME') # generates 1 date each month in the range
countries = ['USA', 'India', 'Brazil', 'UK', 'Russia']

data = {
    'date': np.tile(dates, len(countries)), # repeats entire dates array once for each country
    'country': np.repeat(countries, len(dates)), # repeats every country date for each date
    # generate random data ensuring it has the same length as the number of rows
    'cases': np.random.randint(1000, 1000000, size=len(dates) * len(countries)),
    'deaths': np.random.randint(10, 50000, size=len(dates) * len(countries)),
    'vaccinations': np.random.randint(1000, 5000000, size=len(dates) * len(countries))
}

df = pd.DataFrame(data) # convert data into a table-like dataframe
print(df)

# Save the dataset to a CSV file
df.to_csv('covid_data.csv', index=False)

print("Sample COVID-19 dataset created: covid_data.csv")
