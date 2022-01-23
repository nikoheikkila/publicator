import subprocess
from shlex import split
from typing import List


def run(command: str) -> List[str]:
    if not command:
        return []

    result = subprocess.run(split(command), capture_output=True, check=True, text=True)

    return result.stdout.splitlines()
