Hello! This is a ML-bookcamp midterm project based on the [Kaggle Used Car Auction Prices dataset](https://www.kaggle.com/datasets/tunguz/used-car-auction-prices). The goal is to practice basics of creation Machine Learning model and its deployment with BentoML.

### Problem description

The dataset contains historical information about characteristics of used cars put up for various auctions and its selling prices. I want to create a web service will allows us to predict the initial price of a car on the basis of its type and information about recent transactions. Of course each car has its own characteristics and unique condition, nevertheless, service will allows a potential seller to evaluate his auto in the current market or projected price can be used by an auction as a starting point for further bidding.

### Initialization
Project is created on Yandex Cloud VM under Ubuntu and stored as GitHub repository.

Initial steps:

clone the repo and _car-prices-midterm_ will be the _project folder_ 
>`git clone https://github.com/K0nkere/Car-prices-midterm.git`

from the _project folder_ create conda virtual environment based on the provided _requirements.txt_ and _python 3.9_
> `conda create -n midterm-project python=3.9`

activate the conda env
> `conda activate midterm-project`

installation python packages
> `pip install -r requirements.txt`

If you are using Jupyter Notebook then its need to add venv python to ipykernel list
> `conda install -c anaconda ipykernel`

> `python -m ipykernel install --user --name=midterm-project`

So you can choose _midterm-project_ as a kernel for .ipynb scripts in Jupyter Notebooks's menu

### Files and folders of _project folder_
- _dataset_ folder contains previously downloaded data files that is used for train and test purposes
- _deployment_ folder contains scripts and side files for BentoML deployment
- _project-EDA.ipynb_ Exploration data analysis of dataset
- _model-training-tuning.ipynb_ covers parametes tuning of varios models
- _train-model.py_ script for training best model and saving it with BentoML
- _requirement.txt_ covers python packages for reproduce the project

### Running
1. Activate the conda venv from the _project folder_
> `conda activate midterm-project`

2. Run model trainig process - it will train model on _full train_ dataset and will save it as a BentoML model
> `python ../train-model.py`

3. Check it with
> `bentoml models list`

it will return something like _"car-price-prediction-model:szcugfdangto4loz"_

At this step you can validate the working process by manually launching with API service
> ```cd deployment``` - move to _deployment_ folder
> ```docker ps``` - check that 3000 port is empty, use `docker kill <container_id>` if need
> ```bentoml serve service.py:svc --reload```

Access API service with your browser _localhost:3000_ and you can use the following test - it is 199 row of _test dataset_
```
{
"year": 2014,
 "make": "Ram",
 "model": "2500",
 "trim": "Laramie",
 "body": "Crew Cab",
 "transmission": "automatic",
 "vin": "3c6ur5fl7eg293685",
 "state": "ut",
 "condition": 3.5,
 "odometer": 26499.0,
 "color": "black",
 "interior": "black",
 "seller": "barco rent a truck",
 "mmr": 43300, 
 "sellingprice": 43000, 
 "saledate": "Wed Feb 25 2015 03:30:00 GMT-0800 (PST)"
 }
 ```

### BentoML deployment

From ./deployment folder under the conda environment
bentoml build

bentoml containerize car-price-prediction-service:your_model_tag

docker run -it --rm -p 3000:3000 car-price-prediction-service:your_model_tag serve --production