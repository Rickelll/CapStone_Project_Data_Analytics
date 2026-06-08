import pandas as pd

dataset = pd.read_csv('customer_order_sales_data.csv')

#checking min and max frequency to be able see a good range
print(dataset['Frequency'].min(), dataset['Frequency'].max())

for column in dataset.columns:
    print(dataset[column])