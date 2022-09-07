import subprocess

user = "pi"
password = "raspberry"

def run_command(command: str, check: bool = True) -> "subprocess.CompletedProcess['str']":

    return subprocess.run(
    [
        "sshpass",
        "-p",
        password,
        "ssh",
        "-o",
        "StrictHostKeyChecking=no",
        f"{user}@localhost",
        command,
    ],
    check=check,
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
