import subprocess


subprocess.run(["poetry", "run", "python", "main.py"], cwd="server", check=True)
