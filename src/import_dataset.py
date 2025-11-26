import requests
import os
import logging

BUCKET_FOLDER_URL= "https://assets-datascientest.s3.eu-west-1.amazonaws.com/MLOPS/bentoml/admission.csv"     
TARGET_PATH= "./data/raw"        
       
def import_raw_data():
    '''import data from BUCKET_FOLDER_URL in TARGET_PATH'''

    input_file = BUCKET_FOLDER_URL
    output_file = TARGET_PATH + "/raw.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    print(f'downloading {input_file} as {os.path.basename(output_file)}'    )
    response = requests.get(input_file)

    if response.status_code == 200:
        # Process the response content as needed
        content = response.text
        with open(output_file, "wb") as text_file:
            text_file.write(content.encode('utf-8'))
            text_file.close()
    else:

        print(f'Error accessing the object {input_file}:', response.status_code)

                
def main():
    """ Upload data from AWS s3 in ./data/raw
    """
    import_raw_data()
    logger = logging.getLogger(__name__)
    logger.info('making raw data set')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    main()