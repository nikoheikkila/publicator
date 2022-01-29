from urllib.parse import urlencode
from publicator.git import Repo
from publicator.semver import Semver


class ReleaseException(Exception):
    pass


def new_release_url(repo: Repo, tag: Semver, title: str = "", body: str = "", pre_release: bool = False) -> str:
    if not repo.is_github:
        raise ReleaseException("Current repository is not hosted on github.com")

    base_url = f"https://{repo.server}/{repo.owner}/{repo.name}/releases/new?"
    query = {"tag": tag, "title": title, "body": body, "prerelease": int(pre_release)}

    return base_url + urlencode(query)
