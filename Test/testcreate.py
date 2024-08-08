import requests

BASE_URL = 'http://127.0.0.1:8000/'

# Test data for creating a profile
profile_data = {
    "address": "123 Unique Street",
    "name": "John Doe",
    "photo": ["photo1.jpg", "photo2.jpg"],
    "location": "City",
    "gender": "male",
    "age": 30,
    "interest": ["reading", "sports"],
    "liked": 0,
    "looking_for": "female",
    "overall": 0,
    "bio": "Just a regular guy.",
    "work": "Engineer",
    "edu": "University",
    "zodiac": "Libra",
    "isonmatch": False
}

# Function to create a profile
def create_profile(data):
    response = requests.post(f'{BASE_URL}create/', json=data)
    if response.status_code == 201:
        print("Profile created successfully.")
        print("Response:", response.json())
    else:
        print("Failed to create profile.")
        print("Response:", response.json())


# Function to get all profiles
def get_all_profiles():
    response = requests.get(f'{BASE_URL}all/')
    if response.status_code == 200:
        print("All profiles retrieved successfully.")
        print("Response:", response.json())
    else:
        print("Failed to retrieve profiles.")
        print("Response:", response.json())

# Function to get a profile by address
def get_profile_by_address(address):
    response = requests.get(f'{BASE_URL}address/{address}/')
    if response.status_code == 200:
        print(f"Profile for address {address} retrieved successfully.")
        print("Response:", response.json())
    elif response.status_code == 404:
        print(f"Profile for address {address} not found.")
    else:
        print("Failed to retrieve profile.")
        print("Response:", response.json())

# Testing the functions
create_profile(profile_data)
get_all_profiles()
get_profile_by_address("123 Unique Street")
