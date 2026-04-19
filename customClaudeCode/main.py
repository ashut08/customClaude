

import os
from openai import OpenAI
import json
from dotenv import load_dotenv
from tools import grep, read_file, write_file, edit_file, multi_edit, list_files, run_command, set_project_root, TOOL_SCHEMAS

load_dotenv()

client = OpenAI()

PROJECT_ROOT = os.getcwd()
set_project_root(PROJECT_ROOT)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
file_prompt = open(os.path.join(SCRIPT_DIR, 'prompt.txt'), 'r').read()

system_prompt = f"""
You are an interactive CLI tool that helps users build and maintain Flutter applications.
You can ONLY operate on files within the current project directory: {PROJECT_ROOT}
All file paths must be relative to or within this directory.

{file_prompt}

IMPORTANT: Do NOT respond with JSON. Use the provided tools directly via function calling.
When the task is fully complete, respond with a short summary in plain text.
"""

TOOL_MAP = {
    "grep": grep,
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "multi_edit": multi_edit,
    "list_files": list_files,
    "run_command": run_command,
}

messages = [
    {"role": "system", "content": system_prompt},
]

while True:
    query = input("> ")
    messages.append({"role": "user", "content": query})

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )
        assistant_msg = response.choices[0].message
        messages.append(assistant_msg)

        if assistant_msg.tool_calls:
            for tool_call in assistant_msg.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                print(f"🛠 {tool_name} → {tool_args}")

                try:
                    if tool_name in TOOL_MAP:
                        print("finding tool in TOOL_MAP")
                        result = TOOL_MAP[tool_name](**tool_args)
                        #print(f"tool result: {result}")
                    else:
                        result = f"Unknown tool: {tool_name}"
                except Exception as e:
                    result = f"Error: {e}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })
            continue

        if assistant_msg.content:
            print(f"🤖 {assistant_msg.content}")
        break