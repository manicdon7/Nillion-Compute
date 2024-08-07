import asyncio
from nillion_python_helpers import NillionClient, Transaction

# Initialize the Nillion client
client = NillionClient()

async def store_data(address, ipfs_string, timestamp):
    # Create a transaction to store data
    transaction = Transaction()
    
    # Define the data to be stored
    data = {
        "address": address,
        "IpfsString": ipfs_string,
        "timestamp": timestamp
    }
    
    # Prepare the transaction
    transaction_data = {
        "operation": "store",
        "data": data
    }
    
    # Add transaction data
    transaction.add_data(transaction_data)
    
    # Submit the transaction to the network
    try:
        receipt = await client.submit_transaction(transaction)
        print(f"Transaction receipt: {receipt}")
    except Exception as e:
        print(f"Error submitting transaction: {e}")

async def main():
    # Example data
    address = "0x1234567890abcdef"
    ipfs_string = "QmT5NvUtoM5nM5NjQW8tT5E9M5q2d6E93M39vRjRUV1smu"
    timestamp = "2024-08-06T15:00:00Z"
    
    # Store the data
    await store_data(address, ipfs_string, timestamp)

# Run the script
if __name__ == "__main__":
    asyncio.run(main())
