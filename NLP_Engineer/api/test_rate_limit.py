import requests

url = "http://127.0.0.1:8000/extract-entities"

for i in range(15):
    response = requests.post(
        url,
        json={
            "text": "Beautiful three bedroom home in Irvine"
        }
    )

    print(
        f"Request {i + 1}: "
        f"Status {response.status_code}"
    )

# After 10th request, received Status 429, which means "too many requests." 
# So, the rate limiting is working properly.