BentoML deployment

From ./deployment folder under the conda environment
bentoml build

bentoml containerize car-price-prediction-service:your_model_tag

docker run -it --rm -p 3000:3000 car-price-prediction-service:your_model_tag serve --production