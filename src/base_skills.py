"""Initial base skills available to LLM agents.

This is not src code, but the list of available
task primitives that CodeGen may call through ChromeDB
"""
from typing import List


def GetListOfRestaurantsAt(location: str) -> List[str]:
  """Returns a list of restraurants near location.
  """
  return [
    "BestPizza-%s" % location,
    "BestRamen-%s" % location,
    "BestPub-%s" % location,
    "BestBurger-%s" % location]

def QueryClosestWikipediaMatch(article_name: str) -> List[str]:
  """Returns a list of Wikipedia articles that are a close match to article_name.
  """
  return [
    "History of %s" % article_name,
    "List of Famous %s" % article_name,
    "Early %s" % article_name
  ]