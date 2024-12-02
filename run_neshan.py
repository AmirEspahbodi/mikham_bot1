import subprocess
from concurrent.futures import ThreadPoolExecutor


# Commands to run
subprocess.run(["poetry", "run", "python", "run_scraper.py"], cwd="neshan", check=True)
