# Examen BentoML

Step by Step explanation:

- create virtual environment

- Import the data
    - download the data from https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv
    using src/import_datset.py and save it in data/raw

- src/prepare_data.py: vectornormalize and split the data set from data/raw into "X" and "y", where "y" is "Chance of Admit"
and save it in data/processed

- training
    - with src/train_model.py using RandomForestRegressor taking the processed data from data/processed
    and save the best model and the params in model

- testing the model and saving to BentoML    
    - using src/test_model.py, the model is model and tested with the test data set.
    it saves the predictions, the merits, and the model

- create BentoML API with bentoml serve
- creating the Bento with bentoml build

- testing the api with either the single test or pytest tests/test_all.py
