# Importing necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Step 1: Let's grab some data (titanic dataset - several from Kaggle too)
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
titanic_data = pd.read_csv(url)

#Start - display the first few rows of dataset (to console)
print(titanic_data.head())

#This function will give us info about our dataset
print(titanic_data.info())

#Step 2: Analyzing Survival Rates (first analysis of data)
# --------------------------------------

#What is the overall survival rate
#The logic -> calculated as the mean of Survived column (1 / 0)
#Survival rates are then grouped by passenger class- bar plot to visualize data
survival_rate = titanic_data['Survived'].mean()
print(f"Overall Survival Rate: {survival_rate * 100:.2f}%")

#What is the survival rate by passenger class
survival_by_class = titanic_data.groupby('Pclass')['Survived'].mean()
print(survival_by_class)

#Now let's create a visualization of survival rate by passenger class
sns.barplot(x='Pclass', y='Survived', data=titanic_data)
plt.title('Survival Rate by Passenger Class')
plt.xlabel('Passenger Class')
plt.ylabel('Survival Rate')
plt.show()

#Step 3: Analyzing Age Distribution (next analysis of data)
# --------------------------------------
# Distribution of Age (- dropna - drops missing values)
sns.histplot(titanic_data['Age'].dropna(), kde=True, bins=30) # drops missing data
plt.title('Distribution of Age on Titanic')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.show()

#Box plot of age by survival
sns.boxplot(x='Survived', y='Age', data=titanic_data)
plt.title('Age Distribution by Survival')
plt.xlabel('Survived')
plt.ylabel('Age')
plt.show()

#Step 4: Correlation between Features (Class, Age, and Survival)
# --------------------------------------------------------------

#Correlation matrix between numeric features (heatmap)
correlation_matrix = titanic_data[['Survived', 'Pclass', 'Age', 'Fare']].corr()
print(correlation_matrix)

#Visualize the correlation matrix using a heatmap (id significant correlations)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation between Features')
plt.show()

#Analyze the relationship between age, class, and survival
sns.scatterplot(x='Age', y='Fare', hue='Survived', style='Pclass', data=titanic_data)
plt.title('Age vs Fare: Survived vs Not Survived (Colored by Class)')
plt.xlabel('Age')
plt.ylabel('Fare')
plt.show()

#Step 5: More Advanced Analysis
# -----------------------------------------

#Survival rate by sex
survival_by_sex = titanic_data.groupby('Sex')['Survived'].mean()
print(survival_by_sex)

#Visualization of survival rate by sex
sns.barplot(x='Sex', y='Survived', data=titanic_data)
plt.title('Survival Rate by Sex')
plt.xlabel('Sex')
plt.ylabel('Survival Rate')
plt.show()

#Class, Age, and Survival relationship visualized using FacetGrid
#Visualizes the age distribution across different classes and survival statuses
g = sns.FacetGrid(titanic_data, col='Survived', row='Pclass', margin_titles=True)
g.map(plt.hist, 'Age', bins=20)
plt.show()

#Summary
'''
Survival Rate by Passenger Class: A bar plot shows survival rates for first, second, and third class.
Age Distribution: A histogram shows how ages were distributed among the Titanic passengers.
Correlation Heatmap: Shows correlations between survival, passenger class, age, and fare.
Age vs Fare Scatter Plot: Shows the relationship between age, fare, and survival, colored by class.
'''