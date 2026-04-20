# Custom Claude - AI Coding Agent

A lightweight CLI-based AI coding agent built in Python. It uses GPT-4.1 with native tool calling to autonomously read, write, edit files, and run shell commands — like your own mini Cursor/Claude Code.

## How It Works

```
You → prompt → GPT-4.1 → calls tools → executes → loops back → done
```

The agent runs in a continuous loop:
1. You type a request
2. GPT-4.1 decides which tools to call
3. The agent executes them (read/write/edit files, run commands)
4. Results are fed back to GPT-4.1
5. It keeps going until the task is fully complete

**No frameworks. No LangChain. Just Python + OpenAI API.**

## Project Structure

```
customClaudeCode/
├── main.py        # Agent loop (~84 lines)
├── tools.py       # 7 tools + OpenAI schemas (~200 lines)
├── prompt.txt     # System prompt with coding rules
├── customclaude   # Shell script to run globally
└── .env           # Your API key
```

## Tools Available

| Tool | Description |
|------|-------------|
| `grep` | Search for text patterns across files |
| `read_file` | Read file contents |
| `write_file` | Create or overwrite files |
| `edit_file` | Find and replace in a file |
| `multi_edit` | Multiple find-and-replace in one file |
| `list_files` | List directory contents |
| `run_command` | Execute shell commands |

All file operations are **sandboxed** to the current project directory — the agent can't access files outside your project.

## Setup

### 1. Clone the repo

```bash
git clone git@github.com:ashut08/customClaude.git
cd customClaude
```

### 2. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install openai python-dotenv
```

### 4. Add your API key

Create a `.env` file:

```
OPENAI_API_KEY=your-api-key-here
```

### 5. Run it

```bash
python3 main.py
```

## Run From Anywhere

To use `customclaude` as a global command:

```bash
chmod +x customclaude
```

Edit the `customclaude` file and update the paths to match your setup, then symlink it:

```bash
ln -sf /full/path/to/customclaude ~/.local/bin/customclaude
```

Now `cd` into any project folder and type:

```bash
customclaude
```

## Example Usage

```
> create a flutter project called myapp
🛠 run_command → {'command': 'flutter create myapp'}

> add a todo feature with bloc
🛠 write_file → {'path': 'myapp/lib/todo/bloc/todo_bloc.dart', ...}
🛠 write_file → {'path': 'myapp/lib/todo/bloc/todo_event.dart', ...}
🛠 write_file → {'path': 'myapp/lib/todo/bloc/todo_state.dart', ...}
🛠 write_file → {'path': 'myapp/lib/todo/view/todo_page.dart', ...}
🤖 Created todo feature with bloc pattern.
```

## Customization

- **Change the model** — edit `model="gpt-4.1"` in `main.py`
- **Change the rules** — edit `prompt.txt` to fit your framework/language
- **Add new tools** — define a function in `tools.py`, add its schema to `TOOL_SCHEMAS`, and register it in `TOOL_MAP` in `main.py`

## Tech Stack

- Python 3
- OpenAI API (GPT-4.1 with function calling)
- ~300 lines of code total

## License

MIT — do whatever you want with it.

## Author

Built by [@ashut08](https://github.com/ashut08)
