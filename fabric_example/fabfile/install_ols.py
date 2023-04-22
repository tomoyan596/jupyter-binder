from fabric import task
from invoke.watchers import Responder

from . import CheckInstallation, tmux_run

@task
@tmux_run
def OLS_install(c):
    enterResponder = Responder(
        pattern=r"\n>",
        response="\n"
    )
    result = c.run(
        "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        hide=False, pty=True,
        watchers=[enterResponder])
    #print(result.stdout.strip())

@task
@tmux_run
def OLS_uninstall(c):
    yesResponder = Responder(
        pattern=r"Continue\? \(y/N\)",
        response="y\n"
    )
    result = c.run(
        "rustup self uninstall",
        pty=True,
        watchers=[yesResponder])
