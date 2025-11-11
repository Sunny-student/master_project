# Code you have previously used to load data
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Path of the file to read
iowa_file_path = 'engineerProject/home-data-for-ml-course/train.csv'
home_data = pd.read_csv(iowa_file_path)

# Create target object and call it y
y = home_data.SalePrice

# Create X
features = ['LotArea', 'YearBuilt', '1stFlrSF',
            '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']
X = home_data[features]

# Split into validation and training data
# val_size is set to 0.25 as default
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(
    random_state=1, n_estimators=130)

# fit your model
rf_model.fit(train_X, train_y)

# Calculate the mean absolute error of your Random Forest model on the validation data
rf_val_predictions = rf_model.predict(val_X)

rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("\nValidation MAE for Random Forest Model: {}".format(rf_val_mae))

quantity = np.arange(1, len(rf_val_predictions)+1)

fig = plt.figure(figsize=(14, 5))
plt.plot(quantity, rf_val_predictions, 'r')
plt.plot(quantity, val_y, 'b')
plt.title('Compare Predictions with Validations')
plt.xlabel('Index')
plt.ylabel('SalePrice')
plt.legend(['Predictions', 'Validations'])
plt.show()
