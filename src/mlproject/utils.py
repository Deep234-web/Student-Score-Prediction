import os
import sys
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import pymysql
import dill
from sklearn.metrics import r2_score

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
password=os.getenv("password")
db=os.getenv("db")


def read_sql_data():
    logging.info("Reading sql database started")
    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db
        )

        logging.info(f"Connection established,{mydb}")
        df=pd.read_sql_query("Select * from student",mydb)
        print(df.head())

        return df

    except Exception as e:
        raise CustomException(e)
    


def save_object(file_path,obj):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb")as file_obj:
            dill.dump(obj,file_obj)

    except Exception as e:
        raise CustomException(e,sys)
    


def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report={}
        for i in range(len(list(models))):
            model=list(models.values())[i]


            model.fit(X_train,y_train)
            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)
            train_model_score=r2_score(y_train,y_train_pred)
            test_model_score=r2_score(y_test,y_test_pred)
            report[list(models.keys())[i]]=test_model_score

        return report
    except Exception as e:
        raise CustomException(e,sys)