import time
import statistics
import requests

URL = "http://127.0.0.1:8000/predict"

payload = {
    "features": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
}

latencies = []

for _ in range(20):
    start = time.perf_counter()

    response = requests.post(URL, json=payload)
    response.raise_for_status()

    latency = time.perf_counter() - start
    latencies.append(latency)

print(f"Requests: {len(latencies)}")
print(f"Average latency: {statistics.mean(latencies):.4f} seconds")
print(f"Fastest request: {min(latencies):.4f} seconds")
print(f"Slowest request: {max(latencies):.4f} seconds")