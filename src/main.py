"""
Main.
"""
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

task = "Write me some code to play tictactoe."

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role":
            "system",
        "content":
            "You are a skilled programmer who can solve any task handed to you programmatically."
    }, {
        "role": "assistant",
        "content": "Hello, how can I help you today?"
    }, {
        "role": "user",
        "content": f"Help me with this task: {task}"
    }, {
        "role":
            "assistant",
        "content":
            "Sure, let me first lay out a list of subtasks that may help with the larger goal:"
    }])

response = completion.choices[0]

print(response)

validation_proposal_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role":
            "system",
        "content":
            "You are an AI agent. You work in conjunction with many other AI agents. Your role in the wider system is to figure out how to validate whether a task was completed successfully. You do not need to actually validate whether the task was completed. Your suggestions will be provided to a different agent who will actually validate the task."
    }, {
        "role":
            "user",
        "content":
            f"I was given the following task: {task}. I provided the following solution: {response['message']['content']}. How can I validate if the task was successfully completed?"
    }])

print(validation_proposal_completion.choices[0])

validation_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{
        "role":
            "system",
        "content":
            "You are an AI agent. You work in conjunction with many other AI agents. Given a task and a proposed response, your job is to validate whether the task was successfully completed. You will be provided with a suggestion for how to actually validate the task completion. If you decide the task was not completed successfully, you should provide feedback for what is missing and how to fix it."
    }, {
        "role":
            "user",
        "content":
            f"I was given the following task: {task}. I provided the following solution: {response['message']['content']}. I was also provided the following guidelines for how to validate whether my solution was sufficient for the task: {validation_proposal_completion.choices[0]['message']['content']}. Can you validate whether my solution was sufficient for the task? If it was not, can you provide feedback for how to fix it?"
    }])

print(validation_completion.choices[0])
