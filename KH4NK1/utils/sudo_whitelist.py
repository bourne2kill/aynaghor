# List of commands that are allowed to run with sudo.
# Add new entries here *only* after a security review.
WHITELIST = {
    "apt-get update",
    "apt-get install -y git curl ffmpeg sudo",
    "pip install -U openai-whisper gtts pillow diffusers",
    "pip install -r",
    "git init",
    "git add .",
    "git commit -m",
    "git push",
    # add more as needed
}

def is_allowed(command: str) -> bool:
    # Simple prefix check – if the command starts with any whitelisted token, allow it.
    for token in WHITELIST:
        if command.strip().startswith(token):
            return True
    return False