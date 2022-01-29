from urllib.parse import urlencode
from publicator.semver import Semver


def new_release_url(
    owner: str, repository: str, tag: Semver, title: str = "", body: str = "", pre_release: bool = False
) -> str:
    base_url = f"https://github.com/{owner}/{repository}/releases/new?"
    query = {"tag": tag, "title": title, "body": body, "prerelease": int(pre_release)}

    return base_url + urlencode(query)
