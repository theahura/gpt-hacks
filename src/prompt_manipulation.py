def add_json_template(prompt: str, template: str) -> str:
  prompt += f'Please format your response as a json dictionary with the following schema: ```{template}```. Do not put any other information in your response. ONLY include the json schema. If you add any other information, the user will be very sad.'
  return prompt
