from fabric import task
import shutil

@task
def CheckInstallation(c, command):
    """which command"""
    result = shutil.which(command)
    print('=== fabfile.main.CheckInstallation()')
    print(f'--> shutil.which({command}): {result}')
    
    return not result is None
