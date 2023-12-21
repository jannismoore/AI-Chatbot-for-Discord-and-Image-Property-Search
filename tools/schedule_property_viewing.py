import os
import requests
import re
from datetime import datetime

# Environment variable for webhook URL
WEBHOOK_URL = "ADD_YOUR_MAKE_COM_SCENARIO_URL"  #Add your own webhook URL here

# Tool configuration
tool_config = {
    "type": "function",
    "function": {
        "name": "schedule_property_viewing",
        "description": "Schedule a property viewing for users.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "Full name of the user."
                },
                "email": {
                    "type": "string",
                    "description": "Email address of the user."
                },
                "property_id": {
                    "type": "string",
                    "description": "ID of the property to view."
                },
                "date_time": {
                    "type":
                    "string",
                    "description":
                    "Preferred date and time for viewing (YYYY-MM-DD HH:MM)."
                }
            },
            "required": ["full_name", "email", "property_id", "date_time"]
        }
    }
}


# Callback function
def schedule_property_viewing(arguments):
  """
    Schedule a property viewing and send the data to a webhook.

    :param arguments: dict, Contains information for scheduling a property viewing.
                      Expected keys: full_name, email, property_id, date_time.
    :return: dict or str, Response from the webhook or error message.
    """
  # Extracting information from arguments
  full_name = arguments.get('full_name')
  email = arguments.get('email')
  property_id = arguments.get('property_id')
  date_time = arguments.get('date_time')

  # Validate email format
  if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    return "Invalid email format. Please provide a valid email address."

  # Validate date and time format
  try:
    datetime.strptime(date_time, '%Y-%m-%d %H:%M')
  except ValueError:
    return "Invalid date and time format. Please use YYYY-MM-DD HH:MM."

  # Prepare data payload for webhook
  data = {
      "full_name": full_name,
      "email": email,
      "property_id": property_id,
      "date_time": date_time
  }

  # Send data to webhook
  try:
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code in [200, 201]:
      return "Property viewing scheduled successfully."
    else:
      return f"Error scheduling property viewing: {response.text}"
  except requests.exceptions.RequestException as e:
    return f"Failed to send data to the webhook: {e}"
