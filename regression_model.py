import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

dataset = pd.read_csv("customer_regression_data.csv")



print(dataset.head())

print(dataset.columns)

#The regression model does not use CustomerID, InvoiceNo, current MonetaryValue, or current AverageOrderValue as learning features. These columns are either identifiers or contain information from the current order. Instead, the model uses previous customer behaviour, such as previous monetary value, previous average order value, previous order count, previous order value, days since previous order, and country, to predict the current order value.
X_features = ["PreviousAverageOrderValue",
              "PreviousMonetaryValue",
    "PreviousOrderCount",
    "PreviousOrderValue",
    "DaysSincePreviousOrder",
              "Country"]

#X is our training data and Y is our target data
X = dataset[X_features].values
y = dataset.iloc[:, -1].values

print(X)
print(y)

#Splitting our training data for Random Forest Regression
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#Training our model
regressor = DecisionTreeRegressor(random_state = 0)
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

#Random Forest regression test using previous customer behaviour only:
#Features used: PreviousMonetaryValue, PreviousAverageOrderValue,
#PreviousOrderCount, and PreviousOrderValue.


#Result:
#Mean Absolute Error: 320.92
#Mean Squared Error: 845479.80
#Root Mean Squared Error: 919.50
#R2 Score: 0.26


#The model was able to identify some relationship between previous customer
#behaviour and future order value, but prediction accuracy was limited.
#This suggests that previous customer behaviour alone is not enough to
#accurately predict the next order value. Additional features such as
#product type, customer segment, seasonality, and order timing may improve
#future model performance.
#Regression test using product-row level data:
#Result:
#Mean Absolute Error: 17.70
#Mean Squared Error: 66477.29
#Root Mean Squared Error: 257.83
#R2 Score: 0.97


#This result was rejected because the dataset contained repeated product rows
#from the same invoice. Since multiple rows shared the same InvoiceNo and
#OrderValue, the model performance was likely inflated by data leakage.


#To fix this, the regression dataset was rebuilt as one row per invoice.
#Raw Quantity and UnitPrice were removed from the invoice-level regression
#dataset because each invoice can contain multiple products with different
#quantities and prices.

#Next Test: Trying with DaysSincePreviousOrder and country

#Mean Absolute Error: 327.96
#Mean Squared Error: 1315825.75
#Root Mean Squared Error: 1147.09
#R2 score: 0.25

#Next Test: Testing with DecsionTreeRegressor

