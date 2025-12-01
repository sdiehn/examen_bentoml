import os
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = "./data/raw/raw.csv"   
OUTPUT_PATH = "./data/processed"

os.makedirs(OUTPUT_PATH, exist_ok=True)

def vector_normalize(X):
    ''' Normalize the data using vector normalization
    '''
    X_np = X.values.astype(float)
    norms = np.linalg.norm(X_np, axis=1, keepdims=True)
    X_normalized = X_np /norms
    return pd.DataFrame(X_normalized, columns=X.columns)

def split_data():
    ''' Split raw data into X_test, X_train, y_test,  and y_train
    '''
    raw_data = pd.read_csv(RAW_DATA_PATH)
    output_file = OUTPUT_PATH + "/"

    raw_data = raw_data.iloc[:, 1:]

    X_train, X_test, y_train, y_test = train_test_split(
        raw_data.drop('Chance of Admit ', axis=1),
        raw_data['Chance of Admit '],
        test_size=0.2,
        random_state=42
    )

    X_train.to_csv(os.path.join(output_file, "X_train.csv"), index=False)
    X_test.to_csv(os.path.join(output_file, "X_test.csv"), index=False)
    y_train.to_csv(os.path.join(output_file, "y_train.csv"), index=False)
    y_test.to_csv(os.path.join(output_file, "y_test.csv"), index=False)

    return X_train, X_test, y_train, y_test
    
def normalize_data(data_sub_set):
    ''' Normalize the data using vector normalization
    '''
    data_scaled=vector_normalize(data_sub_set)
    return data_scaled

def scale_and_save_data(X_train, X_test):
    ''' Scale data and save them to output folder
    '''
    X_train_scaled = normalize_data(X_train)
    X_test_scaled = normalize_data(X_test)

    output_file = OUTPUT_PATH + "/"

    X_train_scaled.to_csv(os.path.join(output_file, "X_train_scaled.csv"), index=False)
    X_test_scaled.to_csv(os.path.join(output_file, "X_test_scaled.csv"), index=False)


def main():
    ''' Create final dataset from raw data
    '''
    logger = logging.getLogger(__name__)
    logger.info('preprocessing data set')

    X_train, X_test, y_train, y_test = split_data()
    scale_and_save_data(X_train, X_test)


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    main()