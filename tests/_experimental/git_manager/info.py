from pathlib import Path
from pprint import pprint

from git import Repo


def get_commits():
    current_project = Path(__file__).parent.parent.parent.parent
    print(current_project)
    repo = Repo(current_project)
    commits = list(repo.iter_commits("master", max_count=5))
    cs = [{"name": str(c.author), "email": c.author.email, "msg": c.message, "date": c.committed_date} for c in commits]
    return cs


if __name__ == "__main__":
    m_commits = get_commits()
    for m_commit in m_commits:
        pprint(m_commit)
