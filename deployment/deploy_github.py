import os
import subprocess
from utilities.logger import Logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve GitHub credentials from environment variables
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
GITHUB_PAT = os.getenv("GITHUB_PAT")  # Personal Access Token for authentication
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")  # Default branch is main

class GitHubDeployer:
    """Handles deployment of the bot to a private GitHub repository."""

    def __init__(self, repo_url, branch="main"):
        """Initialize GitHub deployment settings."""
        if not repo_url or not GITHUB_PAT:
            Logger.log_error("❌ GitHub credentials are missing. Check your environment variables.")
            raise ValueError("GitHub credentials not found.")

        self.repo_url = repo_url.replace("https://", f"https://{GITHUB_PAT}@")
        self.branch = branch
        self.local_repo_path = os.getcwd()  # Assume script is run from repo root

    def run_git_command(self, command):
        """Execute a Git command and return the output."""
        try:
            result = subprocess.run(command, cwd=self.local_repo_path, capture_output=True, text=True, shell=True)
            if result.returncode != 0:
                Logger.log_error(f"❌ Git command failed: {command}\n{result.stderr}")
                return None
            return result.stdout.strip()
        except Exception as e:
            Logger.log_error(f"❌ Error executing Git command: {command} | {e}")
            return None

    def initialize_repo(self):
        """Initialize the local Git repository if not already initialized."""
        if not os.path.exists(os.path.join(self.local_repo_path, ".git")):
            Logger.log_system("🔄 Initializing new Git repository...")
            self.run_git_command("git init")
            self.run_git_command(f"git remote add origin {self.repo_url}")
            self.run_git_command(f"git checkout -b {self.branch}")
            Logger.log_system(f"✅ Repository initialized and set to branch: {self.branch}")

    def commit_and_push(self, commit_message="Updated bot files"):
        """Commit changes and push to GitHub."""
        self.run_git_command("git add .")
        commit_output = self.run_git_command(f'git commit -m "{commit_message}"')
        if commit_output:
            Logger.log_system(f"📌 Commit successful: {commit_message}")
        else:
            Logger.log_warning("⚠️ No new changes to commit.")

        push_output = self.run_git_command(f"git push -u origin {self.branch}")
        if push_output:
            Logger.log_system("🚀 Code successfully pushed to GitHub.")
        else:
            Logger.log_error("❌ Failed to push code to GitHub.")

# If running this script independently, trigger deployment
if __name__ == "__main__":
    try:
        deployer = GitHubDeployer(GITHUB_REPO_URL, GITHUB_BRANCH)
        deployer.initialize_repo()
        deployer.commit_and_push("🚀 Auto-deploy: Updated trading bot code")
    except Exception as e:
        Logger.log_error(f"❌ GitHub Deployment failed: {e}")
