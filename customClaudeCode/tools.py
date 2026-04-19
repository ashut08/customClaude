import os
import subprocess

_PROJECT_ROOT = "."

def set_project_root(path):
    global _PROJECT_ROOT
    _PROJECT_ROOT = os.path.abspath(path)

def _safe_path(path):
    resolved = os.path.abspath(os.path.join(_PROJECT_ROOT, path))
    if not resolved.startswith(_PROJECT_ROOT):
        raise PermissionError(f"Access denied: {path} is outside the project folder")
    return resolved
def run_command(command: str):
    try:
        result = subprocess.run(
            ["bash", "-c", command],
            text=True,
            capture_output=True,
            cwd=_PROJECT_ROOT,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return output if output else "command executed"
    except Exception as e:
        return str(e)

def grep(pattern, path="."):
    safe = _safe_path(path)
    matches = []
    for root, _, files in os.walk(safe):
        for file in files:
            full = os.path.join(root, file)
            try:
                with open(full, "r") as f:
                    for i, line in enumerate(f.readlines()):
                        if pattern in line:
                            rel = os.path.relpath(full, _PROJECT_ROOT)
                            matches.append(f"{rel}:{i+1}:{line.strip()}")
            except:
                pass
    return "\n".join(matches[:50])


def read_file(path):
    safe = _safe_path(path)
    with open(safe, "r") as f:
        return f.read()


def write_file(path, content):
    safe = _safe_path(path)
    os.makedirs(os.path.dirname(safe), exist_ok=True)
    with open(safe, "w") as f:
        f.write(content)
    return f"wrote {path}"


def edit_file(path, old, new):
    safe = _safe_path(path)
    with open(safe, "r") as f:
        content = f.read()
    content = content.replace(old, new)
    with open(safe, "w") as f:
        f.write(content)
    return f"updated {path}"


def multi_edit(path, edits):
    safe = _safe_path(path)
    with open(safe, "r") as f:
        content = f.read()
    for e in edits:
        content = content.replace(e["old"], e["new"])
    with open(safe, "w") as f:
        f.write(content)
    return f"multi-updated {path}"


def list_files(path="."):
    safe = _safe_path(path)
    return "\n".join(os.listdir(safe))


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": "Search for a text pattern across files in a directory tree. Returns matching lines with file paths and line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "The text pattern to search for"},
                    "path": {"type": "string", "description": "Root directory to search in", "default": "."}
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return the full contents of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a file with the given content. Creates parent directories if needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write to the file"}
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Replace a specific string in a file with a new string.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to edit"},
                    "old": {"type": "string", "description": "The exact text to find and replace"},
                    "new": {"type": "string", "description": "The replacement text"}
                },
                "required": ["path", "old", "new"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "multi_edit",
            "description": "Apply multiple find-and-replace edits to a single file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file to edit"},
                    "edits": {
                        "type": "array",
                        "description": "List of edits to apply",
                        "items": {
                            "type": "object",
                            "properties": {
                                "old": {"type": "string", "description": "Text to find"},
                                "new": {"type": "string", "description": "Replacement text"}
                            },
                            "required": ["old", "new"]
                        }
                    }
                },
                "required": ["path", "edits"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files and directories in the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory to list", "default": "."}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": "Run a shell command and return the output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run"}
                },
                "required": ["command"]
            }
        }
    }
]