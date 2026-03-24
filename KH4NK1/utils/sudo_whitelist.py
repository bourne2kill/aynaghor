import shlex

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
    """
    Checks if a command is allowed to run with sudo.
    Implements security checks to prevent shell chaining and prefix bypasses.
    """
    # 1. Block shell metacharacters that allow command chaining, redirection, etc.
    # These characters can be used to execute arbitrary commands even if the prefix is whitelisted.
    FORBIDDEN_CHARS = {";", "&", "|", ">", "<", "`", "$", "(", ")", "\n", "\r", "#"}
    if any(char in command for char in FORBIDDEN_CHARS):
        return False

    try:
        # 2. Tokenize the input command using shlex to handle quotes correctly.
        # This ensures we match full words and not just prefixes.
        command_tokens = shlex.split(command.strip())
    except ValueError:
        # Invalid shell syntax (e.g. unclosed quotes)
        return False

    if not command_tokens:
        return False

    # 3. Check against the whitelist using token-based matching.
    # We allow the command if it starts with the exact tokens of any whitelisted entry.
    for entry in WHITELIST:
        try:
            entry_tokens = shlex.split(entry)
        except ValueError:
            continue # Should not happen with hardcoded WHITELIST

        if len(command_tokens) >= len(entry_tokens):
            if command_tokens[:len(entry_tokens)] == entry_tokens:
                return True

    return False
