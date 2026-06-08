import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

dataset = pd.read_csv("customer_regression_data.csv")



print(dataset.head())

print(dataset.columns)

#The regression model does not use CustomerID, InvoiceNo, current MonetaryValue, or current AverageOrderValue as learning features. These columns are either identifiers or contain information from the current order. Instead, the model uses previous customer behaviour, such as previous monetary value, previous average order value, previous order count, previous order value, days since previous order, and country, to predict the current order value.
X_features = ["PreviousMonetaryValue", "PreviousAverageOrderValue", "PreviousOrderCount", "PreviousOrderValue"]

#X is our training data and Y is our target data
X = dataset[X_features].values
y = dataset.iloc[:, -1].values

print(X)
print(y)

#Splitting our training data for Random Forest Regression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#Training our model
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)

#Making Predictions
y_pred = regressor.predict(X_test)

#Evaluting models
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Mean Absolute Error:", round(mae,2))
print("Mean Squared Error:", round(mse,2))
print("Root Mean Squared Error:", round(rmse, 2))
print("R2 score:", round(r2,2))

#Mean Absolute Error: 320.92
#Mean Squared Error: 845479.8
#Root Mean Squared Error: 919.5
#R2 score: 0.26
#with "PreviousMonetaryValue", "PreviousAverageOrderValue", "PreviousOrderCount", "PreviousOrderValue" columns

#The Random Forest regression model was able to identify some relationship between previous customer behaviour and order value, but the prediction accuracy was limited. This suggests that previous customer behaviour alone is not enough to accurately predict future order value. Additional features such as product category, quantity, seasonality, and customer segment may improve future model performance.
#Testing with product and quantity information