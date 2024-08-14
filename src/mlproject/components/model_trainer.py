
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor,GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression, Ridge,Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import warnings
import os
import sys
from src.mlproject.utils import save_object,evaluate_models
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging

from dataclasses import dataclass

@dataclass
class ModelTrainingConfig:
    trained_model_file_path=os.path.join('artifact',"model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainingConfig()


    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Splitting training and test input data")
            X_train,y_train,X_test,y_test=(

                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models={
                "Random Forest":RandomForestRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Linear Regression":LinearRegression(),
                "K-Neighbors":KNeighborsRegressor(),
                "XGBRegression":XGBRegressor(),
                "CatBoosting":CatBoostRegressor(),
                "AdaBoost Regression":AdaBoostRegressor()
            }

            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,models=models)

            best_model_score=max(sorted(model_report.values()))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info("Best found model on both training and testing dataset")


            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model 

            )

            predicted=best_model.predict(X_test)

            r2_square=r2_score(y_test,predicted)
            return r2_square
        
        except Exception as e:
            raise CustomException(e,sys)