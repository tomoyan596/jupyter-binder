from fabric import task
import shutil

@task
def CheckInstallation(c, command):
    result = shutil.which(command)
    print('=== fabfile.main.CheckInstallation()')
    print(f'--> shutil.which: {result}')
    
    return not result is None
