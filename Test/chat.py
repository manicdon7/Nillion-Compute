import requests

BASE_URL = 'http://127.0.0.1:8000/'

# Function to create a chat
def create_chat(participants_addresses):
    params = {'participants': participants_addresses}
    response = requests.get(f'{BASE_URL}create_chat/', params=params)
    if response.status_code == 201:
        print("Chat created successfully.")
        return response.json()
    else:
        print("Failed to create chat.")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None

# Function to send a message
def send_message(chat_id, sender_address, content):
    params = {'chat_id': chat_id, 'sender_address': sender_address, 'content': content}
    response = requests.get(f'{BASE_URL}send_message/', params=params)
    if response.status_code == 201:
        print("Message sent successfully.")
        return response.json()
    else:
        print("Failed to send message.")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None

# Function to get all profiles
def get_all_profiles():
    response = requests.get(f'{BASE_URL}all/')
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve profiles.")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        return None

# Example usage
# Get all profiles to use their addresses
profiles = get_all_profiles()
if profiles:
    # Extract addresses of the first two profiles for testing
    address1 = profiles[0]['address']
    address2 = profiles[1]['address']
    print(f"Using addresses: {address1}, {address2}")

    # Create a chat with the two addresses
    chat = create_chat([address1, address2])
    if chat:
        # Send messages between the participants
        send_message(chat['id'], address1, "Hello from first profile!")
        send_message(chat['id'], address2, "Hi from second profile!")
