import os
import requests
import re

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']

# The tool configuration
tool_config = {
    "type": "function",
    "function": {
        "name": "store_lead",
        "description": "Collects and stores real estate leads in Airtable.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the lead."
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number of the lead.",
                    "pattern": "^\+?[1-9]\d{1,14}$"  # E.164 format
                },
                "email": {
                    "type": "string",
                    "description": "Email address of the lead.",
                    "format": "email"
                },
                "property_preferences": {
                    "type": "string",
                    "description":
                    "Details of the lead's property preferences."
                }
            },
            "required": ["name", "phone", "email", "property_preferences"]
        }
    }
}


# The callback function (Adds lead to Airtable)
def store_lead(arguments):
  """
    Collects and stores real estate leads in Airtable.

    :param arguments: dict, Contains the information for storing a lead.
                      Expected keys: name, phone, email, property_preferences.
    :return: dict or str, Response from the API or error message.
    """
  # Extracting information from arguments
  name = arguments.get('name')
  phone = arguments.get('phone')
  email = arguments.get('email')
  property_preferences = arguments.get('property_preferences')

  # Validating the presence of all required information
  if not all([name, phone, email, property_preferences]):
    return "Missing required information. Please provide name, phone, email, and property preferences."

  # Validate phone number format (E.164 format)
  if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
    return "Invalid phone number format. Please provide a valid phone number."

  # Airtable API URL and headers
  url = f"https://api.airtable.com/v0/appsq0SSPLS4fgtuY/Leads"
  headers = {
      "Authorization": f"Bearer {AIRTABLE_API_KEY}",
      "Content-Type": "application/json"
  }

  # Data payload for the API request
  data = {
      "records": [{
          "fields": {
              "Name": name,
              "Phone": phone,
              "Email": email,
              "Property Preferences": property_preferences
          }
      }]
  }

  # Making the API request with error handling
  try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    return response.json()
  except requests.exceptions.RequestException as e:
    return f"Failed to store lead: {str(e)}"
