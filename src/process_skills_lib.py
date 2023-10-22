"""Library code for chroma.
"""
from typing import TypedDict, List, Optional, Tuple

import os

import chromadb

def ProcessSkillFile(file_py: str) -> List[Tuple]:
  found_skills = []
  with open(file_py, "r") as f:
    s = f.read()

  fn_code = s.split("\ndef ")
  for fn in fn_code[1:]:
    fn_name = fn.split("(")[0]
    fn_args = "(" + fn.split("(")[1].split("\n")[0][:-1]
    descriptor = fn.split("""\"\"\"""")[-2].strip()

    found_skills.append((fn_name, fn_args, descriptor))
  return found_skills

def WriteContextForSkillFile(skills:List[Tuple]) -> str:
  # Oudated and defer to SkillsEmbedding later
  context = """You have the following Python library, their pytype function signature, and description:"""
  context += "\n```"
  for skill in skills:
    context += "\n"
    context += "%s, %s, %s" % skill
  context += "\n```"

  return context

class SkillsEmbedding:
  def __init__(self, base_skill_file, learned_skill_file):
    self.base_skill_file = base_skill_file
    self.learned_skill_file = learned_skill_file

    self.chroma_client = chromadb.Client()
    self.collection = self.chroma_client.create_collection(name="skill_library")

    self.base_skills = ProcessSkillFile(base_skill_file)
    self.learned_skills = ProcessSkillFile(learned_skill_file)
    self.add_skills_file(self.learned_skill_file)
    self.skills = self.base_skills + self.learned_skills

  def add_skills_file(self, skill_file):
    # fn_name, fn_args, descriptor
    skills = ProcessSkillFile(skill_file)
    if len(skills) == 0:
      return
    skill_file_descriptor = ["%s %s" % (s[2], s[0]) for s in skills]
    skill_id = [s[0] for s in skills]
    self.collection.add(documents=skill_file_descriptor, ids=skill_id)

  def search(self, skill_description, n_results):
    if skill_description is not list:
      skill_description = [skill_description]
    res = self.collection.query(query_texts=skill_description, n_results=n_results)
    return res['ids']

  def append_learned_skill_to_file(self, skill_tuple):
    # skill_tuple is of the form [skill_name, skill_description, code_block]
    code_block = skill_tuple[2]
    with open(self.learned_skill_file, 'a') as f:
      f.write(code_block)
      f.write("\n\"\"\"%s\"\"\"\n" % skill_tuple[1])
    # Very lazy as I don't want to reparse this single instance
    self.learned_skills = ProcessSkillFile(self.learned_skill_file)
    self.add_skills_file(self.learned_skill_file)

  def construct_skill_context(self, learned_ids):
    context = ""
    # Writes the base skills and then learned skills
    context += "\n```"
    for skill in self.base_skills:
      context += "\n"
      context += "%s, %s, %s" % skill

    # Write the selected learned skills
    learned_set = set(learned_ids)
    for learned_skill in self.learned_skills:
      if learned_skill[0] in learned_set:
        # found skill add it to context
        context += "\n"
        context += "%s, %s, %s" % learned_skill
    context += "\n```"
    return context

# s = SkillsEmbedding(base_skill_file="src/base_skills.py", learned_skill_file="src/learned_skills.py")
# # s.add_skills_file()
# s.search("Need Information about Restaurants", 2)

# s.append_learned_skill_to_file(("test_fn_write", "This is a test description",
#   """def test_fn_write(x: str)->str:
#   return \"d\""""))
