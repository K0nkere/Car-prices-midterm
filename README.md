Hello! This is a ML-bookcamp midterm project based on the [Kaggle Used Car Auction Prices dataset](https://www.kaggle.com/datasets/tunguz/used-car-auction-prices). The goal is to practice basics of creation Machine Learning model and its deployment with BentoML.

### Problem description

The dataset contains historical information about characteristics of used cars put up for various auctions and its selling prices. I want to create a web service will allows us to predict the initial price of a car on the basis of its type and information about recent transactions. Of course each car has its own characteristics and unique condition, nevertheless, service will allows a potential seller to evaluate his auto in the current market or projected price can be used by an auction as a starting point for further bidding.

### Initialization
Project is created on Yandex Cloud VM under Ubuntu and stored as GitHub repository. 
Initial steps:
clone the repo and __car-prices-midterm__ will be the __project folder__ 
>`git clone https://github.com/K0nkere/Car-prices-midterm.git`
from the __project folder__ create conda virtual environment based on the provided __requirements.txt__ and __python 3.9__
> `conda create -n midterm-project python=3.9`
activate the conda env
> `conda activate midterm-project`
installation python packages
> `pip install -r requirements.txt`
If you are using Jupyter Notebook then its need to add venv python to ipykernel list
> `conda install -c anaconda ipykernel`
> `python -m ipykernel install --user --name=midterm-project`
So you can choose __midterm-project__ as a kernel for .ipynb scripts in Jupyter Notebooks's menu

### Files and folders of __project folder__
- __dataset__ folder contains previously downloaded data files that is used for train and test purposes
- __deployment__ folder contains scripts and side files for BentoML deployment
- __project-EDA.ipynb__ Exploration data analysis of dataset
- __model-training-tuning.ipynb__ covers parametes tuning of varios models
- __train-model.py__ script for training best model and saving it with BentoML
- __requirement.txt__ covers python packages for reproduce the project




### BentoML deployment

From ./deployment folder under the conda environment
bentoml build

bentoml containerize car-price-prediction-service:your_model_tag

docker run -it --rm -p 3000:3000 car-price-prediction-service:your_model_tag serve --production