import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import joblib
import numpy as np
import os

print(joblib.__version__)

DATA_PATH = 'data/processed/'
MODEL_PATH = 'models/'  

X_train = pd.read_csv(DATA_PATH + 'X_train_scaled.csv')
y_train = pd.read_csv(DATA_PATH + 'y_train.csv')
y_train = np.ravel(y_train)

def train_model():
    ''' Train Random Forest Regressor model with hyperparameter tuning
    ''' 
    rf_regression = RandomForestRegressor(n_estimators=100, random_state=42)

    grid_params = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    grid_search = GridSearchCV(
        estimator=rf_regression,
        param_grid=grid_params,
        cv=3,
        n_jobs=-1,
        verbose=2
    )

    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_
    best_model = grid_search.best_estimator_
    return best_model, best_params

def main():
    ''' Main function to train the model and save it
    '''
    best_model, best_params = train_model()

    joblib.dump(best_params, os.path.join(MODEL_PATH, "best_params.pkl"))
    joblib.dump(best_model, os.path.join(MODEL_PATH, "best_model.pkl"))

if __name__ == '__main__':
    main()
    print("Model trained and saved successfully.")