import os
import json
import requests

# Configuration for the make.com webhook
MAKE_COM_WEBHOOK_URL = "ADD_YOUR_MAKE_COM_SCENARIO_URL"

# The tool configuration
tool_config = {
    "type": "function",
    "function": {
        "name": "analyze_image",
        "description":
        "Analyzes an image and extracts valuable Real Estate information.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "URL of the image to be analyzed."
                }
            },
            "required": ["image_url"]
        }
    }
}


# The callback function (Sends image to make.com for analysis)
def analyze_image(arguments):
  """
    Analyze an image using make.com's webhook.

    :param arguments: dict, Contains the image URL.
                      Expected key: image_url.
    :return: dict or str, Summary and details from the analysis or error message.
    """
  image_url = arguments.get('image_url')

  # Validating the presence of the image URL
  if not image_url:
    return "Missing required information. Please provide the image URL."

  # Preparing the payload for the webhook
  data = {"image_url": image_url}

  # Sending the request to the make.com webhook
  response = requests.post(MAKE_COM_WEBHOOK_URL, json=data)

  print(response.json())

  # Check if the response is valid and contains content
  if response.status_code == 200:
    return response.text
  else:
    # Handle invalid response or non-JSON content
    print(f"Invalid response or not JSON: Status Code {response.status_code}")
    return {"error": "Invalid response."}
