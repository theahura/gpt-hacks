"""
Contains base functions for calling out to the openai api.
"""
from typing import TypedDict, List, Optional, Tuple

import os
import openai

import prompt_manipulation


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


def get_access_token():
  # Returns a valid access token from the OS Environment
  return os.getenv("OPENAI_API_KEY")


def call_gpt(messages: List[Message],
             model: str) -> Tuple[Message, GPTChatCompletionUsage]:
  """Calls OpenAI API with the above messages"""
  openai.api_key = get_access_token()
  completion = openai.ChatCompletion.create(model=model, messages=messages)
  return completion.choices[0], completion.usage


def to_gpt_message(role: str, content: str) -> Message:
  return {'role': "user", 'content': content}
