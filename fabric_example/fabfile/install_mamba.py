from fabric import task
from invoke.watchers import Responder

from . import CheckInstallation, tmux_run

@task
@tmux_run
def Mamba_CheckInstalled(c):
    return CheckInstallation(c, 'micromamba')

@task
@tmux_run
def Mamba_Install(c):
    if Mamba_CheckInstalled(c):
        print('Mamba はインストール済みです😉');
        return False
    
    enterResponder = Responder(
        pattern=r'\n>',
        response='\n'
    )
    result = c.run(
        # install.sh が shell を判定するので | bash である必要がある🤔
        #"curl --proto '=https' --tlsv1.2 -sSf https://micro.mamba.pm/install.sh | sh",
        "curl --proto '=https' --tlsv1.2 -sSf https://micro.mamba.pm/install.sh | bash",
        echo=True, hide=False, pty=True,
        watchers=[enterResponder]
    )
    #print(result.stdout.strip())

@task
@tmux_run
def Mamba_Uninstall(c):
    if not Mamba_CheckInstalled(c):
        print('Mamba はインストールされていません🤔');
        return False
    
    yesResponder = Responder(
        pattern=r'Continue\? \(y/N\)',
        response='y\n'
    )
    result = c.run(
        "rustup self uninstall",
        echo=True, pty=True,
        watchers=[yesResponder])
