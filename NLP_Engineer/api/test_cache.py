import requests

url = "http://127.0.0.1:8000/extract-entities"

payload = {
    "text": "Beautiful three bedroom home in Irvine"
}

# First request
response1 = requests.post(url, json=payload)

print("First request:")
print("Status:", response1.status_code)
print("Response:", response1.json())

# Second identical request
response2 = requests.post(url, json=payload)

print("\nSecond request:")
print("Status:", response2.status_code)
print("Response:", response2.json())

# Compare responses
if response1.json() == response2.json():
    print("\n✓ Responses are identical.")
else:
    print("\n✗ Responses are different.")

# I received status 200 for both responses when running this code, but
# in the API terminal where I ran my API, I got a message that "Cache Hit"
# which shows that the memory of the first response was stored properly