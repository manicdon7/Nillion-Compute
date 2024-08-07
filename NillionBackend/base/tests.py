import requests

# Define the URL of the endpoint
url = 'http://localhost:8000/store-program'  # Replace with the actual URL

# Define the parameters
params = {
    'age_int2': 18,
    'location_int1': 2,
    'match_gender_int': 0,
    'age_int1': 30,
    'looking_for_gender_int': 0
}

# Make the GET request
response = requests.get(url, params=params)

# Print the response
if response.status_code == 200:
    print("Success!")
    print("Response JSON:", response.json())
else:
    print("Failed!")
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
