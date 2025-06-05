# Data Analysis Project

This document outlines the **data analysis process** using _Python_ and its most common libraries.

## 1. Objectives

- Load and clean data
- Analyze descriptive statistics
- Visualize data using plots

## 2. Sample Python Code

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('data.csv')

# Show basic statistics
print(df.describe())

# Bar chart
df['category'].value_counts().plot(kind='bar')
plt.title("Category Distribution")
plt.show()
```

## 3. Data Table

| Name     | Age | City       |
|----------|-----|------------|
| Ana      | 23  | Bogotá     |
| Luis     | 30  | Medellín   |
| Camila   | 27  | Cali       |

## 4. Highlighted Quote

> "Without data, you're just another person with an opinion."  
> — W. Edwards Deming

## 5. Additional Notes

- Data should be in CSV format.
- Use virtual environments to avoid dependency conflicts.
- Always check for missing values before analysis.
