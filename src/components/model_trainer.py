from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from xgboost import XGBRegressor
from src.exception import CustomeException
import logging
from src.utils import evaluate_model, save_object
from dataclasses import dataclass
import os
import sys


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_tainer(self,train_arr,test_arr):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                    "Random Forest" : RandomForestRegressor(),
                    "Decision Tree" : DecisionTreeRegressor(),
                    "KNN"           : KNeighborsRegressor(),
                    "XGB Boost"     : XGBRegressor(),
                    "Gradiant Boost": GradientBoostingRegressor(),
                    "ADA Boost"     : AdaBoostRegressor()  
            }

            model_report:dict=evaluate_model(X_train=X_train,y_train=y_train,
                                             X_test=X_test,y_test=y_test,
                                             models=models)
            
            #To get a best model score from dict
            best_model_score = max(sorted(model_report.values()))

            #To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_name)
            ]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomeException("No best model found")
            logging.info(f"Best model found")

            save_object (
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test,predicted)
            return r2_square


        except Exception as e:
            raise CustomeException(e,sys)

