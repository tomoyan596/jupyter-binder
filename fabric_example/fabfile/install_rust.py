from fabric import task
from invoke.watchers import Responder

from . import CheckInstallation, tmux_run

@task
@tmux_run
def Rust_CheckInstalled(c):
    result = CheckInstallation(c, 'rustup')
    return result

@task
@tmux_run
def Rust_Install(c):
    if Rust_CheckInstalled(c):
        print('Rust はインストール済みです😉');
        return False
    
    enterResponder = Responder(
        pattern=r'\n>',
        response='\n'
    )
    result = c.run(
        "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        echo=True, hide=False, pty=True,
        watchers=[enterResponder])
    result = c.run(
        "$SHELL -l",
        echo=True, hide=False, pty=True,
        watchers=[enterResponder])
    #print(result.stdout.strip())

@task
@tmux_run
def Rust_Uninstall(c):
    if not Rust_CheckInstalled(c):
        print('Rust はインストールされていません🤔');
        return False
    
    yesResponder = Responder(
        pattern=r'Continue\? \(y/N\)',
        response='y\n'
    )
    result = c.run(
        'rustup self uninstall',
        echo=True, pty=True,
        watchers=[yesResponder]
    )
