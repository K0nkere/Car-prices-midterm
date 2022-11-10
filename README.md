Hello! This is a ML-bookcamp midterm project based on the [Kaggle Used Car Auction Prices dataset](https://www.kaggle.com/datasets/tunguz/used-car-auction-prices). The goal is to practice basics of cretion Machine Learning model and its deployment with BentoML.

### Problem description

The dataset contains historical information about characteristics of used cars put up for various auctions and its selling prices. I want to create a web service will allows us to predict the initial price of a car on the basis of its type and information about recent transactions. Of course each car has its own characteristics and unique condition, nevertheless, service will allows a potential seller to evaluate his auto in the current market or projected price can be used by an auction as a starting point for further bidding.

### Initialization
Project is created on Yandex Cloud VM under Ubuntu and stored as GitHub repository. 
Initial steps:
> clone the repo
    `git clone https://github.com/K0nkere/Car-prices-midterm.git`


### BentoML deployment

From ./deployment folder under the conda environment
bentoml build

bentoml containerize car-price-prediction-service:your_model_tag

docker run -it --rm -p 3000:3000 car-price-prediction-service:your_model_tag serve --production