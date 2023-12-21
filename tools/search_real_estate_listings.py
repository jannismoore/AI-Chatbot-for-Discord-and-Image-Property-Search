import os
import requests

RAPID_API_KEY = os.environ['RAPID_API_KEY']

# The tool configuration
tool_config = {
    "type": "function",
    "function": {
        "name": "search_real_estate_listings",
        "description":
        "Search for real estate listings based on various parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type":
                    "string",
                    "description":
                    "Location to search (city, zip code, or address)."
                },
                "offset": {
                    "type": "number",
                    "description": "Offset results. Default is 0."
                },
                "limit": {
                    "type": "number",
                    "description":
                    "Number of results to return. Default is 50."
                },
                "beds": {
                    "type":
                    "integer",
                    "description":
                    "Number of bedrooms. Sets both minimum and maximum."
                },
                "baths": {
                    "type":
                    "integer",
                    "description":
                    "Number of bathrooms. Sets both minimum and maximum."
                },
                "price": {
                    "type":
                    "integer",
                    "description":
                    "Price point. Adjusts for a range around the specified value."
                },
                "home_size": {
                    "type":
                    "integer",
                    "description":
                    "Home size in square feet. Adjusts for a range around the specified size."
                },
                # Include other optional parameters here...
            },
            "required": ["location"]
        }
    }
}


# The callback function (Searches real estate listings)
def search_real_estate_listings(arguments):
  """
    Search for real estate listings using the Rapid API.

    :param arguments: dict, Contains the search parameters.
    :return: dict or str, Response from the API or error message.
    """
  # API endpoint and headers
  url = "https://us-real-estate-listings.p.rapidapi.com/for-sale"
  headers = {
      "X-RapidAPI-Key": RAPID_API_KEY,
      "X-RapidAPI-Host": "us-real-estate-listings.p.rapidapi.com"
  }

  # Preparing query parameters
  query_params = {
      key: arguments.get(key)
      for key in arguments if arguments.get(key) is not None
  }

  # Handling additional parameters
  if "beds" in arguments:
    beds = arguments.get("beds")
    query_params["beds_min"] = beds
    query_params["beds_max"] = beds

  if "baths" in arguments:
    baths = arguments.get("baths")
    query_params["baths_min"] = baths
    query_params["baths_max"] = baths

  if "price" in arguments:
    price = arguments.get("price")
    query_params["price_min"] = max(0, price - 20000)
    query_params["price_max"] = price + 20000

  if "home_size" in arguments:
    home_size = arguments.get("home_size")
    query_params["home_size_min"] = max(0, home_size - 300)
    query_params["home_size_max"] = home_size + 300

  # Making the API request
  try:
    response = requests.get(url, headers=headers, params=query_params)
    response.raise_for_status()
    return response.json()
  except requests.exceptions.RequestException as e:
    return f"Error: {str(e)}"
