from asyncio import subprocess
import os
import subprocess
import sys
import venv
from pathlib import Path

def print_step(message):
    print(f"\n\033[1;34m[STEP]\033[0m {message}")

def print_success(message):
    print(f"\033[1;32m[SUCCESS]\033[0m {message}")

def print_error(message):
    print(f"\033[1;31m[ERROR]\033[0m {message}")

def check_python_version():
    min_version = (3, 14)
    if sys.version_info < min_version:
        print_error(f"Python {min_version[0]}.{min_version[1]} or higher is required.")
        print_error(f"Your current version: {sys.version.split()[0]}")
        print("\nPlease install a newer version of Python and try again.")
        sys.exit(1)

def setup():
    check_python_version()
    project_dir = Path(__file__).parent.absolute()
    venv_dir = project_dir / "venv"
    env_file = project_dir / ".env"
    req_file = project_dir / "requirements.txt"

    print("\033[1;36m=== Async E-Commerce Scraper Setup ===\033[0m")

    # 1. Create Virtual Environment
    if not venv_dir.exists():
        print_step("Creating virtual environment...")
        venv.create(venv_dir, with_pip=True)
        print_success("Virtual environment created.")
    else:
        print_step("Virtual environment already exists. Skipping creation.")

    # Determine pip and python paths
    if os.name == "nt":  # Windows
        pip_path = venv_dir / "Scripts" / "pip.exe"
        python_path = venv_dir / "Scripts" / "python.exe"
    else:  # macOS/Linux
        pip_path = venv_dir / "bin" / "pip"
        python_path = venv_dir / "bin" / "python"

    # 2. Install dependencies
    if req_file.exists():
        print_step("Installing dependencies...")
        try:
            subprocess.check_call([str(pip_path), "install", "-r", str(req_file)])
            subprocess.call("playwright install chromium")
            print_success("Dependencies installed.")
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install dependencies: {e}")
            sys.exit(1)
    else:
        print_error("requirements.txt not found!")


    print("\n\033[1;32m=== Setup Complete! ===\033[0m")
    print("You can now run the scraper using: ./run.sh")

if __name__ == "__main__":
    try:
        setup()
    except KeyboardInterrupt:
        print("\n\033[1;33m[CANCELLED]\033[0m Setup interrupted by user.")
        sys.exit(0)