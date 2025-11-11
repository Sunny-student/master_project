# import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             mean_squared_log_error)
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

# Read the data
X = pd.read_csv(
    'engineerProject/home-data-for-ml-course/train.csv', index_col='Id')
X_test_full = pd.read_csv(
    'engineerProject/home-data-for-ml-course/test.csv', index_col='Id')

# Remove rows with missing target, separate target from predictors
X.dropna(axis=0, subset=['SalePrice'], inplace=True)
y = X.SalePrice
X.drop(['SalePrice'], axis=1, inplace=True)

# Break off validation set from training data
X_train_full, X_valid_full, y_train, y_valid = train_test_split(
    X, y, train_size=0.8, test_size=0.2, random_state=0)

# "Cardinality" means the number of unique values in a column
# Select categorical columns with relatively low cardinality (convenient but arbitrary)
low_cardinality_cols = [cname for cname in X_train_full.columns if X_train_full[cname].nunique() < 10 and
                        X_train_full[cname].dtype == "object"]

# Select numeric columns
numeric_cols = [cname for cname in X_train_full.columns if X_train_full[cname].dtype in [
    'int64', 'float64']]

# Keep selected columns only
my_cols = low_cardinality_cols + numeric_cols
X_train = X_train_full[my_cols].copy()
X_valid = X_valid_full[my_cols].copy()
X_test = X_test_full[my_cols].copy()

# One-hot encode the data (to shorten the code, we use pandas)
X_train = pd.get_dummies(X_train)
X_valid = pd.get_dummies(X_valid)
X_test = pd.get_dummies(X_test)
X_train, X_valid = X_train.align(X_valid, join='left', axis=1)
X_train, X_test = X_train.align(X_test, join='left', axis=1)

# Define the model
my_model_1 = XGBRegressor(
    n_estimators=1000, eta=0.01, max_depth=4, subsample=0.6, colsample_bytree=0.9)

# Fit the model
my_model_1.fit(X_train, y_train)

# Get predictions
predictions_1 = my_model_1.predict(X_valid)

# Calculate MAE
mae_1 = mean_absolute_error(y_valid, predictions_1)
mse = mean_squared_error(y_valid, predictions_1)
msle = mean_squared_log_error(y_valid, predictions_1)

# Uncomment to print MAE
print("\nMean Absolute Error:", mae_1)
print("Mean Squared Error:", mse)
print("Mean Squared Log Error:", msle)


quantity = np.arange(1, len(predictions_1)+1)
# print(predictions_1)
# print(y_valid)

fig = plt.figure(figsize=(14, 5))
plt.plot(quantity, predictions_1, 'r')
plt.plot(quantity, y_valid, 'b')
# plt.xticks(np.linspace(0, 300, 31))
plt.title('Compare Predictions with Validations')
plt.xlabel('Index')
plt.ylabel('SalePrice')
plt.legend(['Predictions', 'Validations'])
plt.show()
