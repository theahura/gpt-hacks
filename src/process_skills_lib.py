"""Library code for chroma.
"""

def ProcessSkillFile(file_py: str):
  found_skills = []
  with open(file_py, "r") as f:
    s = f.read()

  fn_code = s.split("\ndef ")
  for fn in fn_code[1:]:
    fn_name = fn.split("(")[0]
    fn_args = "(" + fn.split("(")[1].split("\n")[0][:-1]
    descriptor = fn.split("""\"\"\"""")[1].strip()

    found_skills.append((fn_name, fn_args, descriptor))
  return found_skills

def WriteContextForSkillFile(skills):
  context = """You have the following Python library, their pytype function signature, and description:"""
  for skill in skills:
    context += "\n"
    context += "%s, %s, %s" % skill

  return context

# def EmbedSkillFile(file)
print(WriteContextForSkillFile(ProcessSkillFile("src/base_skills.py")))
