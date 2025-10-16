'''
First - install
pip install matplotlib seaborn pandas
This is an example of creating a data visualization dashboard - using matplotlib
and seaborn.
Load sample data -
Shows Bar Plot (seaborn), Pie chart (matplotlib)
Layout - plt.subplots - allows us to create a multi-panel figure
You can customize further
- add more plots (line graphs, scatter plots, etc)
- incorporating user input to change data dynamically
- use tools like Dash or Streamlit - interactive web-based dashboard
'''
#Data first
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

#dataset - here
np.random.seed(0)
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Values': np.random.randint(1, 100, size=4),
    'Subcategory': np.random.choice(['X', 'Y'], size=4)
}
df = pd.DataFrame(data)

#aesthetic style of the plots
sns.set(style="whitegrid")

#figure for the dashboard
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

#bar plot using seaborn
sns.barplot(x='Category', y='Values', data=df, ax=axs[0], palette='viridis')
axs[0].set_title('Bar Plot of Values by Category')
axs[0].set_ylabel('Values')

#pie chart using matplotlib
axs[1].pie(df['Values'], labels=df['Category'], autopct='%1.1f%%', startangle=140)
axs[1].axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
axs[1].set_title('Pie Chart of Values by Category')

#dashboard
plt.tight_layout()
plt.show()
