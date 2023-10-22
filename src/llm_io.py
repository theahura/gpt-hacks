"""
Contains base functions for calling out to the openai api.
"""
import os
import openai

from typing import TypedDict, List, Optional, Tuple


class Message(TypedDict):
  role: str
  content: str
  finish_reason: str


class Response(TypedDict):
  index: int
  message: Message


class GPTChatCompletionUsage(TypedDict):
  prompt_tokens: int
  completion_tokens: int
  total_tokens: int


class GPTChatCompletionResponse(TypedDict):
  id: str
  object: str
  created: int
  model: str
  choices: List[Message]
  usage: GPTChatCompletionUsage


def GetAccessTokens():
  # Returns a valid access token from the OS Environment
  return os.getenv("OPENAI_API_KEY")


def _call_gpt(messages: List[Message],
              model: str) -> Tuple[Message, GPTChatCompletionUsage]:
  """Calls OpenAI API with the above messages"""
  openai.api_key = GetAccessTokens()
  completion = openai.ChatCompletion.create(model=model, messages=messages)
  return completion.choices[0], completion.usage


def query(prompt: str,
          json_template: Optional[str] = None,
          model: Optional[str] = "gpt-3.5-turbo"):

  if json_template is not None:
    prompt += f'Please format your response as a json dictionary with the following schema: ```{json_template}```. Do not put any other information in your response. ONLY include the json schema. If you add any other information, the user will be very sad.'

  return _call_gpt([{'role': "user", 'content': prompt}], model)
