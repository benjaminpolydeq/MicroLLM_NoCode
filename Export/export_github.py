from git import Repo

def push_to_github():
    repo_path = "./"
    repo = Repo(repo_path)
    repo.git.add("data/*.json")
    repo.git.add("rules/*.json")
    repo.git.commit("-m", "Mise à jour dataset et règles")
    origin = repo.remote(name="origin")
    origin.push()
