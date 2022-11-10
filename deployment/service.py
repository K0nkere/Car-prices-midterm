import numpy as np
import pandas as pd

import bentoml
from bentoml.io import JSON, NumpyNdarray

from pydantic import BaseModel

class CarApplication(BaseModel):
    year: int
    make: str
    model: str
    trim: str
    body: str
    state: str
    condition: float
    odometer: float
    seller: str
    saledate: str
 

model_ref = bentoml.xgboost.get(tag_like="car-price-prediction-model:latest")

ordinal = model_ref.custom_objects["OrdinalEncoder"]
scaler = model_ref.custom_objects["StandardScaler"]
dv = model_ref.custom_objects["DictVectorizer"]

model_runner = model_ref.to_runner()

svc = bentoml.Service("car-price-prediction-service", runners=[model_runner])

# @svc.api(input=JSON(), output=JSON())

@svc.api(input=JSON(pydantic_model=CarApplication), output=JSON())
async def predictor(car_application):
    
    application_data=car_application.dict()

    features = ['year',
        'make',
        'model',
        'trim',
        'body',
        'state',
        'condition',
        'odometer',
        'seller',
        'age'
        ]

    record = pd.DataFrame([application_data])
    
    try:
        record["age"] = pd.to_datetime(record.saledate).apply(lambda x: x.year) - record.year
    except:
        return "Please input in valid format 'year': int and 'saledate': dd-mm-yyyy H:M as examlpe"

    record = record[features]

    for col in record.select_dtypes(["object"]).columns:
        record[col] = record[col].str.lower().str.replace(" ", "_")

    numerical_features = record.select_dtypes("number").columns.to_list()

    record["seller"] = ordinal.transform(record["seller"].values.reshape(-1,1))
    record[numerical_features + ["seller"]] = scaler.transform(record[numerical_features + ["seller"]])

    vector = record.to_dict(orient='records')

    sample = dv.transform(vector)
    
    prediction = float(await model_runner.predict.async_run(sample))

    result = {
            "price_estimation": np.expm1(prediction).round(1),
            "model_version": str(model_ref.tag)
        }

    print(result)

    return result