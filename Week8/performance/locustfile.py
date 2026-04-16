from locust import HttpUser, task, between

class APIPerformanceTest(HttpUser):
    wait_time = between(1, 3)

    @task(2)
    def list_users(self):
        self.client.get("/v1/users")

    @task(1)
    def create_user(self):
        self.client.post("/v1/users", json={
            "name": "LoadTest",
            "email": "load@test.com"
        })
