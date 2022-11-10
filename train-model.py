import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.feature_extraction import DictVectorizer

import bentoml

from xgboost import XGBRegressor

def read_data(file):

    data = pd.read_csv(f"./dataset/car_prices_{file}.csv", sep=',', header='infer')

    return data

def data_preprocession(data, features):
    """
    """

    mask = data.sellingprice > 1
    df = data[mask].copy()
    features = features.copy()
        
    df.dropna(inplace=True)

    df["age"] = pd.to_datetime(df.saledate).apply(lambda x: x.year) - df.year
    features.append("age")

    for col in df.select_dtypes(["object"]).columns:
        df[col] = df[col].str.lower().str.replace(" ", "_")
    
    df.sellingprice = np.log1p(df.sellingprice)
        
    return df[features]


def train_model(df, model, params):
    """
    """

    df_full_train = df.copy()
    y_full_train = df_full_train.pop("sellingprice")

    numerical_features = df_full_train.select_dtypes("number").columns.to_list()

    ordinal = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1, encoded_missing_value=-1)

    df_full_train["seller"] = ordinal.fit_transform(df_full_train["seller"].values.reshape(-1,1))

    scaler = StandardScaler()

    df_full_train[numerical_features + ["seller"]] = scaler.fit_transform(df_full_train[numerical_features + ["seller"]])

    dict_full_train = df_full_train.to_dict(orient="records")
                
    dv = DictVectorizer(sparse=True)
    X_full_train = dv.fit_transform(dict_full_train)

    regressor = model(**params)

    regressor.fit(X_full_train, y_full_train, eval_set = [(X_full_train, y_full_train)])

    return ordinal, scaler, dv, regressor


if __name__ == "__main__":

    features = [
        'year',
        'make',
        'model',
        'trim',
        'body',
        'state',
        'condition',
        'odometer',
        # 'color',
        # 'interior',
        # 'transmission',
        'seller',
        'sellingprice',
        ]

    data = read_data(file = "full_train")
    df = data_preprocession(data, features=features)

    params = {
        "eta": 0.2,
        "n_estimators": 250,
        "max_depth": 12,
        "min_child_weight": 8,
        "nthread": -1,

        "objective": "reg:squarederror",
        "eval_metric": "rmse"
        }

    model = XGBRegressor

    ordinal, scaler, dv, regressor = train_model(df=df, model=model, params=params)

    bentoml.xgboost.save_model(
                            name="car-price-prediction-model",
                            model=regressor,
                            custom_objects={
                                "OrdinalEncoder": ordinal,
                                "StandardScaler": scaler,
                                "DictVectorizer": dv
                                }
                            )

