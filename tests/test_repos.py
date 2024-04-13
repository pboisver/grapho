import os
from typing import Optional

from github import Auth, Github, GithubException
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def test_fetch():
    auth = Auth.Token(os.environ["GHTOKEN"])
    with Github(auth=auth) as g:
        print(g.get_rate_limit())

        org = g.get_organization("Display-lab")
        repo = org.get_repo("knowledge-base")
        content = repo.get_contents("readme.md")
        print(repo.visibility)
        print(content)

        try:
            branch = repo.get_branch("mpog_pilot")
            measures = repo.get_contents("measures.json", ref=branch.name)
            causal_pathways = repo.get_contents("causal_pathways", ref=branch.name)
        except GithubException as e:
            print(e)
            return

        print(measures)
        print(causal_pathways)

        print(g.get_rate_limit())


def test_pfp_releases():
    auth = Auth.Token(os.environ["GHTOKEN"])
    with Github(auth=auth) as g:
        print(g.get_rate_limit())

        repo = g.get_repo("Display-lab/precision-feedback-pipeline")

        release = repo.get_release("v0.2.0")
        print({(a.name, a.browser_download_url) for a in release.assets})


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            ".env",
            ".env.local",
        ),
        extra="ignore",
    )
    templates: Optional[HttpUrl] = None
    pathways: Optional[str] = None
    plot_goal_line: Optional[bool] = False
    display_window: Optional[int] = None


# Load settings from the .env file


def test_settings():
    settings = Settings()

    assert settings.display_window == 1

    print(settings.model_dump_json(indent=2))
