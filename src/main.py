"""
Main.
"""
import json
import llm_io

task = "Give me a list of all of the best restaurants in Brooklyn for foodies."

response, usage = llm_io.query(
    prompt=
    'I have the following task, provided to me by a human user: {task}. Can you help me break this down into subtasks?',
    json_template='''
{
  "subtasks": [{
    "name": string
    "requiresMoreSubtasks": boolean  # whether the subtask would benefit from being broken down further
  }, ...]
}
''')

print(response)

subtasks = json.loads(response['message']['content'])['subtasks']
print(subtasks)

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
