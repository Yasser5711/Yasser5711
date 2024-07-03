import requests
from github import Github
import os

USERNAME = "yasser5711"
REPO = USERNAME


token = os.getenv("GH_TOKEN")
g = Github(token)
user = g.get_user(USERNAME)
repo = g.get_repo(REPO)


projects = sorted(
    [r for r in user.get_repos() if not r.fork],
    key=lambda r: r.updated_at,
    reverse=True
)[:6]

markdown_lines = []
for p in projects:
    markdown_lines.append(
        f"- [{p.name}]({p.html_url}) — ⭐ {p.stargazers_count} | 🖥️ {p.language or 'Unknown'}")

content = "\n".join(markdown_lines)


readme = repo.get_readme()
readme_content = readme.decoded_content.decode()

start = "<!--START_SECTION:projects-->"
end = "<!--END_SECTION:projects-->"

new_content = f"{start}\n{content}\n{end}"


updated = readme_content.split(
    start)[0] + new_content + readme_content.split(end)[1]

repo.update_file(
    path=readme.path,
    message="📦 Auto-update latest projects",
    content=updated,
    sha=readme.sha
)
