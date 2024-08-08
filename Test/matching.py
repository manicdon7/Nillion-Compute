import requests

BASE_URL = 'http://127.0.0.1:8000/'

# Profiles to be created
profiles = [
    {
        "address": "456 Second Street",
        "name": "Alice Smith",
        "photo": ["alice1.jpg", "alice2.jpg"],
        "location": "City",
        "gender": "female",
        "age": 28,
        "interest": ["reading", "sports", "cooking"],
        "liked": 0,
        "looking_for": "male",
        "overall": 0,
        "bio": "Loves to read and cook.",
        "work": "Engineer",
        "edu": "University",
        "zodiac": "Cancer",
        "isonmatch": False
    },
    {
        "address": "789 Third Street",
        "name": "Bob Johnson",
        "photo": ["bob1.jpg", "bob2.jpg"],
        "location": "City",
        "gender": "male",
        "age": 32,
        "interest": ["sports", "traveling"],
        "liked": 0,
        "looking_for": "female",
        "overall": 0,
        "bio": "Enjoys traveling and outdoor activities.",
        "work": "Doctor",
        "edu": "Medical School",
        "zodiac": "Aries",
        "isonmatch": False
    },
    {
        "address": "1010 Fourth Street",
        "name": "Charlie Davis",
        "photo": ["charlie1.jpg", "charlie2.jpg"],
        "location": "City",
        "gender": "male",
        "age": 26,
        "interest": ["music", "reading"],
        "liked": 0,
        "looking_for": "female",
        "overall": 0,
        "bio": "Loves music and reading books.",
        "work": "Musician",
        "edu": "Conservatory",
        "zodiac": "Leo",
        "isonmatch": False
    },
    {
        "address": "1112 Fifth Street",
        "name": "Diana Brown",
        "photo": ["diana1.jpg", "diana2.jpg"],
        "location": "City",
        "gender": "female",
        "age": 29,
        "interest": ["traveling", "cooking", "music"],
        "liked": 0,
        "looking_for": "male",
        "overall": 0,
        "bio": "Passionate about cooking and traveling.",
        "work": "Chef",
        "edu": "Culinary School",
        "zodiac": "Virgo",
        "isonmatch": False
    },
    {
        "address": "1314 Sixth Street",
        "name": "Eve Miller",
        "photo": ["eve1.jpg", "eve2.jpg"],
        "location": "City",
        "gender": "female",
        "age": 31,
        "interest": ["sports", "fitness", "traveling"],
        "liked": 0,
        "looking_for": "male",
        "overall": 0,
        "bio": "Fitness enthusiast and world traveler.",
        "work": "Personal Trainer",
        "edu": "Sports Science",
        "zodiac": "Sagittarius",
        "isonmatch": False
    }
]

# Function to create a profile
def create_profile(data):
    response = requests.post(f'{BASE_URL}create/', json=data)
    if response.status_code == 201:
        print(f"Profile {data['name']} created successfully.")
    else:
        print(f"Failed to create profile {data['name']}.")
        print("Response:", response.json())

# Function to get matching profiles by address
def get_matching_profiles(address):
    response = requests.get(f'{BASE_URL}match/{address}/')
    if response.status_code == 200:
        print("Matching profiles retrieved successfully.")
        for match in response.json():
            print(match)
            print(f"Match Percentage: {match['match_percentage']}%")
            print("Profile:", match['profile'])
    elif response.status_code == 404:
        print(f"Profile with address {address} not found.")
    else:
        print("Failed to retrieve matching profiles.")
        print("Response:", response.json())

# Create the profiles
# for profile in profiles:
#     create_profile(profile)

# Test the matching functionality
test_address = "1010 Fourth Street"
get_matching_profiles(test_address)
