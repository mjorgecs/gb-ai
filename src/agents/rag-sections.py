import os

# Define the directory containing the .md files
filepath = '/Users/goodbarber/Desktop/mario-internship/ai-concept-repo/src/data/sections.md'

with open(filepath, 'r') as file:
    content = file.read()

    for line in file:
        print(line)
    print(f"Content:\n  {content}")
