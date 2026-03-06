import requests

BASE_URL = "http://localhost:5000"

def call_code_on_demand():
   
    response = requests.get(f"{BASE_URL}/code-on-demand")

    if response.status_code == 200:
        print("--- Thực thi code nhận được (exec) ---")
        exec(response.text)  


if __name__ == "__main__":
    call_code_on_demand()
