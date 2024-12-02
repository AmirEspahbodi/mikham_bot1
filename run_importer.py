import subprocess


subprocess.run(
    ["poetry", "run", "python", "run_importer.py"], cwd="importer", check=True
)
