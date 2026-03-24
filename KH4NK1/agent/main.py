import subprocess, os, uuid, time, shlex
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

app = FastAPI(title="KH4NK1 AI‑Agent")

# ---------- Pydantic models ----------
class TaskRequest(BaseModel):
    action: str                     # run_shell, create_file, install_deps, etc.
    parameters: Dict[str, Any] = {}

class TaskResponse(BaseModel):
    status: str
    output: str = ""
    error: str = ""

# ---------- Helper utilities ----------
def run_shell(command: str, sudo: bool = False) -> subprocess.CompletedProcess:
    """Execute a shell command with optional sudo."""
    if sudo:
        # whitelist check (see utils/sudo_whitelist.py)
        from utils.sudo_whitelist import is_allowed
        if not is_allowed(command):
            raise PermissionError("Command not whitelisted for sudo")
        command = f"sudo {command}"

    args = shlex.split(command)
    return subprocess.run(
        args,
        shell=False,
        capture_output=True,
        text=True,
        timeout=120,
    )

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# ---------- API endpoints ----------
@app.get("/status")
def status():
    return {"status": "alive", "pid": os.getpid()}

@app.post("/execute/task", response_model=TaskResponse)
def execute_task(req: TaskRequest):
    try:
        if req.action == "run_shell":
            cmd = req.parameters.get("command")
            sudo = req.parameters.get("sudo", False)
            if not cmd:
                raise ValueError("Missing 'command' parameter")
            result = run_shell(cmd, sudo=sudo)
            return TaskResponse(
                status="completed",
                output=result.stdout,
                error=result.stderr,
            )

        elif req.action == "create_file":
            path = req.parameters["path"]
            content = req.parameters.get("content", "")
            write_file(path, content)
            return TaskResponse(status="completed", output=f"File created at {path}")

        elif req.action == "install_deps":
            req_path = req.parameters["requirements_path"]
            sudo = req.parameters.get("sudo", False)
            result = run_shell(f"pip install -r {req_path}", sudo=sudo)
            return TaskResponse(
                status="completed",
                output=result.stdout,
                error=result.stderr,
            )
        else:
            raise ValueError(f"Unsupported action: {req.action}")

    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
