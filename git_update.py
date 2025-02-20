import os
import git

def update_bot():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        repo = git.Repo(repo_dir)
        origin = repo.remotes.origin
        origin.pull()
        print("✅ Trading Bot successfully updated from GitHub!")
    except Exception as e:
        print(f"⚠ Error updating the bot: {e}")

if __name__ == "__main__":
    update_bot()
