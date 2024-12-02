import subprocess


# Commands to run
subprocess.run(["poetry", "run", "python", "run_scraper.py"], cwd="google", check=True)
