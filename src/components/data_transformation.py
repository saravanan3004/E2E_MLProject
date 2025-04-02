import sys
import os
import dataclasses
import numpy as np
import pandas as pd
import logging
from src.exception import CustomeException
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.utils import save_object

@dataclasses
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
            # Instance creation
        config = DataTransformationConfig()
        print(config.preprocessor_obj_file_path)

    def get_data_tranformer_object(self):

        '''This fuction is reposible for data trnsformation'''

        try:
            Numerical_Column = ['lunch', 'test_preparation_course', 'math_score', 'reading_score',
                                'writing_score', 'science_score', 'total_score']
            Categorical_Column = ['roll_no', 'gender', 'race_ethnicity', 'parental_level_of_education',
                                 'grade']
            
            num_pipeline = Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
                    ])

            logging.info("Numerical Columns encoding & std scaling is completed:{Numerical_Column}")

            cat_pipeline = Pipeline(
                    steps=[
                        ("imputer",SimpleImputer(strategy="most_frequent")),
                        ("One_hot_encoder",OneHotEncoder()),
                        ("scaler",StandardScaler())
                ])
            logging.info("Categorical Columns encoding is completed:{Categorical_Column}")

            preprocessor = ColumnTransformer(
                [
                ("numerical_Pipeline",num_pipeline,Numerical_Column)
                ("Categorical_Pipeline",cat_pipeline,Categorical_Column)
                ])
        
            return preprocessor
    
        except Exception as e:
            raise CustomeException(e,sys)
        

    def initiate_data_transformation(self,train_path,test_path):
            
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Read Train & Test data is completed")

            logging.info("Obtaining preprocessing Objects")

            preprocessing_obj = self.get_data_tranformer_object()
            target_column = "total_score"

            input_feature_train_df = train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df = train_df[target_column]

            input_feature_test_df = test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df = test_df[target_column]

            logging.info(f"Apply preprocessing for both Train and Test df")

            input_feature_train_array = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_array =preprocessing_obj.fit(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_array, np.array(target_feature_train_df)
            ]
            test_arr = np.c_[
                input_feature_test_array, np.array(target_feature_test_df)
            ]

            save_object (
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )



        except Exception as e:
            raise CustomeException(e,sys)
            

