import subprocess

# Start child process in the background with DEVNULL for stdin, stdout, and stderr
process = subprocess.Popen(
    ["poetry", "run", "python", "run_scraper.py"],
    cwd="google",
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Continue with the parent process

# import subprocess


# # Commands to run
# subprocess.run(, check=True)
