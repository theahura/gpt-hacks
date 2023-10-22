"""
Main.
"""
import json
from typing import Callable, List, TypedDict, Optional, Tuple

import llm_io
import prompt_manipulation


class Subtask(TypedDict):
  task: str
  requiresMoreSubtasks: bool


class Context(TypedDict):
  context: str
  isOpinion: bool


def get_subtasks(task: str, context: List[Context]) -> List[Subtask]:
  prompt = f'I have the following task, provided to me by a human user: {task}. Can you help me break this down into subtasks?'
  prompt = prompt_manipulation.add_json_template(prompt,
                                                 template='''
{
  "subtasks": [{
    "task": string
    "requiresMoreSubtasks": boolean  # whether the subtask would benefit from being broken down further
  }, ...]
}
''')

  response, _ = llm_io.call_gpt([llm_io.to_gpt_message("user", prompt)])
  return json.loads(response['content'])['subtasks']


def get_context(task: str) -> List[Context]:
  prompt = f'I have the following task, provided to me by a human user: {task}. What additional context should I know that will help me with this task? Please provide at least five pieces of context, but do not hesitate to provide more. In addition, please mark whether you think a given piece of context is a known fact, or an opinion.'
  prompt = prompt_manipulation.add_json_template(prompt,
                                                 template='''
{
  "context": [{
    "context": string
    "isOpinion": bool
  }]
}
''')

  response, _ = llm_io.call_gpt([llm_io.to_gpt_message('user', prompt)])
  return json.loads(response['content'])['context']


class GPTReturnedFunction(TypedDict):
  name: str
  args: List[str]
  returnType: str
  rawFunctionTextWithComments: str


def write_code(task: str, context: List[Context],
               skills: List[str]) -> Tuple[GPTReturnedFunction, str]:
  prompt = f'I have the following task, provided to me by a human user: {task}. I additionally have the following context, provided by an AI agent to help me reason about how to solve the task: {context}. I also have an API with the following function signatures that I can call on: {skills}. Given this information, please write python code that can solve the task. Try and use as many of the passed in functions as possible. In addition, please make sure the code you write is as reusable as possible.'
  response, _ = llm_io.call_gpt([llm_io.to_gpt_message('user', prompt)])

  prompt = f'I have the following message from an AI agent: {response["content"]}. Can you take this message and pull out any individual functions, and store them in a list? I need the full text of the function so that I can use it for eval later. If the function is not populated, i.e. just has `pass` in the body, just ignore it.'
  prompt = prompt_manipulation.add_json_template(prompt,
                                                 template='''
{
  "functions": [{
    name: string
    args: List[string]
    returnType: string
    rawFunctionTextWithComments: string
  }]
}
''')
  function_response, _ = llm_io.call_gpt(
      [llm_io.to_gpt_message('user', prompt)])

  prompt = f'I have the following message from an AI agent: {response["content"]}. Can you take this message and only return the code?'
  prompt = prompt_manipulation.add_json_template(prompt,
                                                 template='''
{
  "code": string
}
''')
  code_response, _ = llm_io.call_gpt([llm_io.to_gpt_message('user', prompt)])

  return json.loads(function_response['content'])['functions'], json.loads(
      code_response['content'])['code']


def solve_task(task: str) -> str:
  context_list = get_context(task)
  print(f'For task {task} got the following context: ', context_list)
  generated_code = write_code(task, context_list, [
      'def get_coords_from_city_name(city: str) -> Tuple[float, float]',
      'def get_restaurants_near_coords(coords: Tuple[float, float]) -> List[str]',
      'def get_restaurant_rating(name: str) -> int'
  ])
  print(f'For task {task}, generated the following code: ', generated_code[0],
        generated_code[1])

  # Run the code and see if it works?
  # try to solve the task
  # validate that the task was solved
  # if the task wasnt solved, loop back with additional context
  return 'hello'


def handle_task(task: str) -> str:
  context_list = get_context(task)
  subtasks = get_subtasks(task, context_list)
  for subtask in subtasks:
    if subtask['requiresMoreSubtasks']:
      handle_task(subtask['task'])
  return 'hello'


if __name__ == '__main__':
  task = "Give me a list of all of the best restaurants in Brooklyn for foodies."
  print(handle_task(task))

# for subtask in subtasks:
#   print(subtask)
#
# print(response)
#
# validation_proposal_completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{
#         "role":
#             "system",
#         "content":
#             "You are an AI agent. You work in conjunction with many other AI agents. Your role in the wider system is to figure out how to validate whether a task was completed successfully. You do not need to actually validate whether the task was completed. Your suggestions will be provided to a different agent who will actually validate the task."
#     }, {
#         "role":
#             "user",
#         "content":
#             f"I was given the following task: {task}. I provided the following solution: {response['message']['content']}. How can I validate if the task was successfully completed?"
#     }])
#
# print(validation_proposal_completion.choices[0])
#
# validation_completion = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{
#         "role":
#             "system",
#         "content":
#             "You are an AI agent. You work in conjunction with many other AI agents. Given a task and a proposed response, your job is to validate whether the task was successfully completed. You will be provided with a suggestion for how to actually validate the task completion. If you decide the task was not completed successfully, you should provide feedback for what is missing and how to fix it."
#     }, {
#         "role":
#             "user",
#         "content":
#             f"I was given the following task: {task}. I provided the following solution: {response['message']['content']}. I was also provided the following guidelines for how to validate whether my solution was sufficient for the task: {validation_proposal_completion.choices[0]['message']['content']}. Can you validate whether my solution was sufficient for the task? If it was not, can you provide feedback for how to fix it?"
#     }])
#
# print(validation_completion.choices[0])
