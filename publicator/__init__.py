from importlib import metadata

name = "publicator"


def display_name() -> str:
    return name.capitalize()


def version() -> str:
    return f"{display_name()} v{metadata.version(name)}"
