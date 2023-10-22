"""
Contains base functions for calling out to the openai api.
"""
import os
import openai


def GetAccessTokens():
  # Returns a valid access token from the OS Environment
  return os.getenv("OPENAI_API_KEY")

def CallGPT(messages, llm_config=None, usage_stats=None):
  """Calls OpenAI API with the above messages"""
  if llm_config is None:
    llm_config = {}


  model = llm_config.get("model", "gpt-3.5-turbo")
  openai.api_key = GetAccessTokens()      
  completion = openai.ChatCompletion.create(
      model=model,
      messages=messages)
  if usage_stats is not None:
    for k in completion.usage:
      if k not in usage_stats:
        usage_stats[k] = 0
      usage_stats[k] += completion.usage[k]
  return completion.choices[0]
