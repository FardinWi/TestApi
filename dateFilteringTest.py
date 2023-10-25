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

    # Iterate through the data to filter events within the date range
    filtered_data = []

    for employee in api_data:
        filtered_events = []
        for event in employee["Events"]:
            if start_date <= event["Date"] <= end_date:
                filtered_events.append(event)
        
        if filtered_events:
            # If there are matching events for this employee, add them to the result
            employee_copy = employee.copy()  # Copy the employee data
            employee_copy["Events"] = filtered_events  # Replace the events with filtered events
            filtered_data.append(employee_copy)

    # Print the filtered data
    for employee in filtered_data:
        print(employee)
else:
    print("Failed to retrieve data from the API. Status code:", response.status_code)
