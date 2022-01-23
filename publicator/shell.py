import subprocess
from shlex import split

def run(command: str) -> list[str]:
    if not command: return []

    result = subprocess.run(split(command), capture_output=True, check=True, text=True)

    return result.stdout.splitlines()
