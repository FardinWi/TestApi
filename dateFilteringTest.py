import requests

# Define the API endpoint
api_url = "http://localhost:8000/eventRecord"  # Replace with the actual API URL

# Define the date range
start_date = "2023-08-25"
end_date = "2023-08-26"

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    api_data = response.json()

    # Filter the data based on the date range
    filtered_data = [event for event in api_data if start_date <= event["Date"] <= end_date]

    # Print the filtered data
    for event in filtered_data:
        print(event)
else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)
