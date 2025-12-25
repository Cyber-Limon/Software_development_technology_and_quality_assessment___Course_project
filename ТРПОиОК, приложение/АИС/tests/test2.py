"""
cd /home/ais/lab-app/АИС
/opt/venv313/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2 --log-level debug >> debug.log 2>&1 &

pkill -f uvicorn
"""

# locust -f tests/test2.py --host=http://192.168.56.104:8000



import random
from requests.auth import HTTPBasicAuth
from locust import HttpUser, task, tag, between



class RESTServerUser(HttpUser):
    wait_time = between(1.0, 2.0)

    def on_start(self):
        self.client.auth = HTTPBasicAuth('admin', 'admin')

    @task(5)
    def get_companies(self):
        with self.client.get("/api/company", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(1)
    def get_room_by_id(self):
        room_id = random.randint(1, 6)
        with self.client.get(f"/api/room/{room_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(5)
    def get_rooms_by_company_id(self):
        company_id = random.randint(1, 3)
        with self.client.get(f"/api/room/company/{company_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(1)
    def get_user_by_id(self):
        user_id = random.randint(1, 5)
        with self.client.get(f"/api/user/{user_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(5)
    def get_users_by_company_id(self):
        company_id = random.randint(1, 3)
        with self.client.get(f"/api/user/company/{company_id}", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(10)
    def update_user(self):
        user_id = random.randint(1, 5)
        data = {"full_name": "Петров"}
        with self.client.put(f"/api/user/{user_id}", json=data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(10)
    def update_room(self):
        room_id = random.randint(1, 6)
        data = {"description": "Обновлено"}
        with self.client.put(f"/api/room/{room_id}", json=data, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")

    @task(10)
    def create_indication_event(self):
        sensor_id = random.randint(1, 18)
        value = 30 + random.randint(-20, 20)
        data = {
            "sensor_id": sensor_id,
            "value": value
        }
        with self.client.post(f"/api/monitoring", json=data, catch_response=True) as response:
            if response.status_code == 201:
                response.success()
            else:
                response.failure(f"Status code is {response.status_code}")
