"""Initial base skills available to LLM agents.

This is not src code, but the list of available
task primitives that an LLM may call through ChromeDB
"""

def GetListOfRestaurantsAt(location_string):
  """Finds a list of restraurants near location_string.

  Args: 
    location_string (str): A string of the location to search for restaruants

  Returns:
    A list of restaurants that are in location_string
  """
  return [
    "BestPizza-%s" % location_string,
    "BestRamen-%s" % location_string,
    "BestPub-%s" % location_string,
    "BestBurger-%s" % location_string]


