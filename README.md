# Regression Project

## What is Multiple Linear Regression?
Regression is a statistical method used to analyze the relationship between two or more independent variables (often denoted as X1, X2, X3, etc.) and a dependent variable (often denoted as Y). It extends the concept of simple linear regression, where only one independent variable is used to predict the dependent variable.

## About the Project
In this project, the core objective is to develop a custom multiple linear regression model using a specifically chosen dataset. The project consists of three main stages:

1. **Data Cleaning**: Address issues like missing data, duplicates, and outliers to ensure the dataset is in optimal condition for training.
2. **Model Training**: Train the model using the cleaned dataset, allowing it to establish relationships between independent and dependent variables, fine-tuning its coefficients for accurate predictions.
3. **Prediction**: Use the trained model to make predictions based on new data.

### Flask API
To interact with the model, we will develop a Flask API with the following capabilities:
- Submit a dataset for cleaning.
- Initiate the model training process.
- Utilize the trained model to make predictions.

### Docker Integration
To enhance accessibility and deployment, we will incorporate Docker. Docker allows us to encapsulate the entire application, including dependencies and environment settings, into a container. This ensures consistency across different environments and simplifies deployment.

## Technologies Used
- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- Docker

## How to Run the Project
1. Clone this repository.
2. Build the Docker container: `docker build -t regression_project .`
3. Run the container: `docker run -p 5000:5000 regression_project`
4. Access the API at `http://localhost:5000`

## License
This project is licensed under the MIT License.
