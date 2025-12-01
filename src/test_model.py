import pandas as pd 
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import bentoml
import json
import joblib
import numpy as np
import os

print(joblib.__version__)

DATA_PATH = 'data/processed/'
PREDICTION_PATH = 'data/predictions/'
MODEL_PATH = 'models/'  
METRICS_PATH = 'metrics/'

CLASSIFIER_NAME = "random_forest_regressor_model"

if not os.path.exists(PREDICTION_PATH):
    os.makedirs(PREDICTION_PATH)

if not os.path.exists(METRICS_PATH):
    os.makedirs(METRICS_PATH)    

X_test = pd.read_csv(DATA_PATH + 'X_test_scaled.csv')
y_test = pd.read_csv(DATA_PATH + 'y_test.csv')
y_test = np.ravel(y_test)

loaded_model = joblib.load(MODEL_PATH + 'best_model.pkl')

def predict_model(X_test):
    ''' Predict using the trained Random Forest Regressor model
    ''' 
    predictions = loaded_model.predict(X_test)
    return predictions  

def get_merits(y_test, predictions):
    ''' Calculate and return model performance metrics
    '''
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    return {
        'MAE': mae,
        'RMSE': rmse,
        'R2_Score': r2
    } 

def save_predictions(predictions):
    ''' Save predictions to a CSV file
    '''
    output_file = PREDICTION_PATH + "predictions.csv"
    pd.DataFrame(predictions, columns=['Chance of Admit']).to_csv(output_file, index=False)   

def save_merits(merits):
    ''' Save model performance metrics to a text file
    '''
    output_file = METRICS_PATH + "scores.json"
    json.dump(merits, open(output_file, 'w'))

def save_bento(name, model):
    ''' Save the model as a BentoML service
    '''
    bentoml.sklearn.save_model(name, model)    
    print(f"BentoML model '{name}' saved successfully.")


def main():
    ''' Main function to make predictions on test data
    '''
    predictions = predict_model(X_test)
    merits= get_merits(y_test, predictions)

    save_predictions(predictions)
    save_merits(merits)
    save_bento(CLASSIFIER_NAME, loaded_model)

    print("Model Performance on Test Data:")
    for key, value in merits.items():
        print(f"{key}: {value}")


if __name__ == '__main__':
    main()