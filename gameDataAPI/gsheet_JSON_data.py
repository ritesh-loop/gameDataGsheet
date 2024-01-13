import requests

url = "https://script.google.com/macros/s/AKfycbxv5aJgGXKQgVcpBFzrXdFsSJSyNO8f72gyU7Wbk0W3piHie3IZlXO41eW5McsNRxU/exec"

response = requests.get(url)

# Print response headers
print("Response Headers:")
for key, value in response.headers.items():
    print(f"{key}: {value}")


# Check the status code
if response.status_code == 200:
    try:
        # Attempt to parse JSON
        data = response.json()
        print(data)
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print("Response Content:", response.content)
else:
    print(f"Error fetching data. Status Code: {response.status_code}")
    print("Response Content:", response.content)
