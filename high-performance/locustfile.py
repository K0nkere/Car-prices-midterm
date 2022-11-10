import numpy as np
from locust import task
from locust import between
from locust import HttpUser

sample = {
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

class CarPricesTestUser(HttpUser):
    """
    Usage:
        Start locust load testing client with:
            locust -H http://localhost:3000
        Open browser at http://0.0.0.0:8089, adjust desired number of users and spawn
        rate for the load test from the Web UI and start swarming.
    """

    @task
    def predictor(self):
        self.client.post("/predictor", json=sample)

    wait_time = between(0.01, 2)