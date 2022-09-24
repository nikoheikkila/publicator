from urllib.parse import urlencode

from safe_assert import safe_assert
from semmy import Semver

from publicator.git import Repo


def new_release_url(repo: Repo, tag: Semver, title: str = "", body: str = "") -> str:
    safe_assert(repo.is_github, "Current repository is not hosted on github.com")

    base_url = f"https://{repo.server}/{repo.owner}/{repo.name}/releases/new?"
    query = {"tag": tag, "title": title, "body": body, "prerelease": int(tag.is_pre_release())}

    return base_url + urlencode(query)
