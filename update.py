import os
import subprocess
import time
import pathlib
import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """Check if there is an active internet connection."""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False

def update_repo(repo_path):
    """Pull the latest changes from the GitHub repository."""
    try:
        print("Checking for updates...")
        result = subprocess.run(["git", "pull"], cwd=repo_path, capture_output=True, text=True)
        if "Already up to date." in result.stdout:
            print("No updates available.")
        else:
            print("Update successful:", result.stdout)
    except Exception as e:
        print("Error updating repository:", str(e))

def main():
    """Main function to check for updates and run main.py."""
    current_path = pathlib.Path(__file__).parent.resolve()
    main_script = current_path / "main.py"
    
    print("Checking internet connection...")
    if check_internet():
        update_repo(current_path)
    else:
        print("No internet connection. Skipping update check.")
    
    print("Starting main.py...")
    subprocess.Popen(["python", str(main_script)])
    
if __name__ == "__main__":
    main()
