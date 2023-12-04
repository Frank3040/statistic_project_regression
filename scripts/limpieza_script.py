import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score

class Manager:
    def __init__(self, data_file):
        self.data = pd.read_csv(data_file)
        self.scaler_cnt = MinMaxScaler()
        
    def LimpiezaTotal(self):
        # Drop unnecessary columns
        self.data = self.data.drop(['instant', 'dteday', 'casual', 'registered'], axis=1)

        # Handle categorical variables
        categorical_cols = ['season', 'weathersit', 'mnth', 'weekday']
        self.data[categorical_cols] = self.data[categorical_cols].astype('category')
        # One-hot encode categorical variables
        self.data = pd.get_dummies(self.data, drop_first=True, dtype='uint8')  # Especifica dtype='uint8'
        # Drop missing values
        self.data = self.data.dropna()
        # Scale numerical features
        scaler = MinMaxScaler()
        num_vars = ['temp', 'atemp', 'hum', 'windspeed']
        self.data[num_vars] = scaler.fit_transform(self.data[num_vars])
        self.scaler_cnt.fit(self.data[['cnt']])
        self.data['cnt'] = self.scaler_cnt.transform(self.data[['cnt']])
        # Save cleaned data to a new CSV file
        #self.data.to_csv('dataset_limpio.csv', index=False)
        return self.data


    def train_and_evaluate_model(self, train_size):
        # Read cleaned data
        if self.data is None:
            self.data = pd.read_csv("../saved_files/dataset_limpio.csv")

        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            self.data.drop('cnt', axis=1), self.data['cnt'],
            train_size=train_size, test_size=1-train_size, random_state=333
        )

        lm = LinearRegression()

        # Feature selection using RFE
        rfe = RFE(lm, n_features_to_select=15)
        rfe = rfe.fit(X_train, y_train)

        # Select the columns from the original DataFrame
        X_train_rfe = X_train.loc[:, rfe.support_]

        # Build linear regression model
        X_train_lm1 = sm.add_constant(X_train_rfe)
        self.lr_model = sm.OLS(y_train, X_train_lm1).fit()

        #Print the summary of the model
        #print(self.lr_model.summary())
        
        # Select the features based on RFE for evaluation
        X_test_rfe = X_test.iloc[:, rfe.support_]
        #print(X_test_rfe)
        # Add a constant to the features
        X_test_lm1 = sm.add_constant(X_test_rfe)
        # Predict using the trained model
        y_pred = self.lr_model.predict(X_test_lm1)
        return self.lr_model
    
    def predict_single_value(self, input_features):
        
        if len(input_features) != len(self.lr_model.params) - 1:
            raise ValueError("The number of features provided for prediction must match the model parameters.")
        X_pred = pd.DataFrame([input_features], columns=self.lr_model.params.index[1:])
        X_pred.insert(0, 'const', 1)
        prediction_scaled = self.lr_model.predict(X_pred)
        prediction = self.scaler_cnt.inverse_transform([prediction_scaled])
        return pd.Series(prediction[0])  # Convertir el array de numpy a una serie de pandas
        