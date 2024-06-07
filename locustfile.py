import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/")
        self.client.get("/episodes")
        self.client.get("episodes/1")
        self.client.get("/episode/3:%20Getting%20Away,%20Now!")
        self.client.get("http://localhost:8000/search", params={"query": "checking email"})