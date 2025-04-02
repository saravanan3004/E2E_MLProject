import os
import sys
import logging
#from src.components.data_transformation import DataTransformationConfig
from src.exception import CustomeException 
from src.components.data_transformation import DataTransformation
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts',"train_csv")
    test_data_path: str = os.path.join('artifacts',"test_csv")
    raw_data_path: str = os.path.join('artifacts',"raw_csv")

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Enters into  DataIngestion method or component")
        try:
            df=pd.read_csv('Jupiter_Notebook\Data\Stud_data.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),mode=0o700,exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False)

            logging.info("Train & Test Split Initiated")

            train_set, test_set = train_test_split(df, test_size=.20, random_state=1) 
            train_set.to_csv(self.ingestion_config.train_data_path,index=False)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False)

            logging.info("Ingestion of data is completed")

            return(
                self.ingestion_config.test_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomeException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
