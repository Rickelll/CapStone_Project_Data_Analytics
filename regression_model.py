import pandas as pd


dataset = pd.read_csv("customer_regression_data.csv")

print(dataset.head())

print(dataset.columns)

X_features = ["PreviousMonetaryValue", "PreviousAverageOrderValue", "PreviousOrderCount", "PreviousOrderValue"]

X = dataset[X_features].values
y = dataset.iloc[:, -1].values

print(X)
print(y)