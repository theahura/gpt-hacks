"""Initial base skills available to LLM agents.

This is not src code, but the list of available
task primitives that CodeGen may call through ChromeDB
"""
from typing import List, Any, Tuple


def GetListOfRestaurantsAt(gps_coordinate: Tuple[float, float]) -> List[str]:
  """Returns a list of restaurants near gps_coordinate.
  """
  return [
    "BestPizza-%s" % location,
    "BestRamen-%s" % location,
    "BestPub-%s" % location,
    "BestBurger-%s" % location]


def GetGPSCoordinateOf(name: str) -> List[Tuple[float, float]]:
  """Returns a list of GPS coordinates for cities with a particular name."""


def GetWeatherDescriptionAt(gps_coordinate: Tuple[float, float]) -> str:
  """Returns a summary describing the most recent weather conditions at a GPS coordinate.
  """

def AccessWikipediaArticle(article_name: str) -> str:
  """Returns information about article_name's Wikipedia article."""
  return "Wikipedia information about %s" % article_name

# Under the hood this is running an LLM to answer question given article
def AnswerQuestionFromArticle(article: str, question: str) -> Any:
  """Answers a question using the Wikipedia article."""
  return 100
