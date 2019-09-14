#первое обучение модельки
import pandas as pd

melbourne_file_path = 'melb_data.csv'
melbourne_data = pd.read_csv(melbourne_file_path)
print(melbourne_data.columns)

melbourne_data = melbourne_datazx

y = melbourne_data.Price

melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

X = melbourne_data[melbourne_features]

print(X.describe())
print(X.head())

from sklearn.tree import DecisionTreeRegressor

melbourne_model = DecisionTreeRegressor(random_state=1)

print(melbourne_model.fit(X, y))

print("Making predictions for the following 5 houses:")
print(X.head())
print("The predictions are")
print(melbourne_model.predict(X.head()))
print(melbourne_data["Price"].head())


#----------------
from sklearn.metrics import mean_absolute_error

predicted_home_prices = melbourne_model.predict(X)
mean_absolute_error(y, predicted_home_prices)

from sklearn.model_selection import train_test_split

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
melbourne_model = DecisionTreeRegressor(random_state = 0)

melbourne_model.fit(train_X, train_y)

val_predictions = melbourne_model.predict(val_X)
print(mean_absolute_error(val_y, val_predictions))
