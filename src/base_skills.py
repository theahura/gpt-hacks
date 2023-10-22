"""Initial base skills available to LLM agents.

This is not src code, but the list of available
task primitives that CodeGen may call through ChromeDB
"""
from typing import List, Any, Tuple


def GetListOfRestaurantsAt(gps_coordinate: Tuple[float, float]) -> List[str]:
  return [
      "BestPizza-%s" % location,
      "BestRamen-%s" % location,
      "BestPub-%s" % location,
      "BestBurger-%s" % location
  ]


"""Returns a list of restaurants near gps_coordinate."""


def GetGPSCoordinateOf(name: str) -> Tuple[float, float]:
  pass


"""Returns a GPS coordinate for a city."""


def GetWeatherDescriptionAt(gps_coordinate: Tuple[float, float]) -> str:
  pass


"""Returns a summary describing the most recent weather conditions at a GPS coordinate."""


def AccessWikipediaArticle(article_name: str) -> str:
  return "Wikipedia information about %s" % article_name


"""Returns information about article_name's Wikipedia article."""

# Under the hood this is running an LLM to answer question given article


def AnswerQuestionFromArticle(article: str, question: str) -> Any:
  return 100


"""Answers a question using information from a Wikipedia article."""
