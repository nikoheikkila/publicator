import subprocess

def run(command: str) -> list[str]:
    return subprocess.run(command.split(), stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()