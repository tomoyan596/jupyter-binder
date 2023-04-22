from fabric import task, Task
from invoke.watchers import Responder
import inspect
import libtmux

TMUX_SESSION_NAME = 'Fabric'

@task
def ConnectTmux(c):
    server = libtmux.Server()
    #session = server.sessions.get(session_name=TMUX_SESSION_NAME)
    session = server.sessions.filter(lambda x: x.session_name.startswith(TMUX_SESSION_NAME))
    if len(sessions) == 0:
        session = server.new_session(session_name=f'{TMUX_SESSION_NAME}')

def detach(c):
    detachResponder = Responder(
        pattern=r'^b^d',
        response='^Bd'
    )
    result = c.run(
        "^b^d",
        hide=False, pty=True,
        watchers=[detachResponder]
    )
    """
    server = libtmux.Server()
    sessions = server.sessions.filter(lambda x: x.session_name.startswith(TMUX_SESSION_NAME))
    #print(sessions)
    if len(sessions) != 0:
        session = sessions[0]
        window = session.attached_window
        pane = window.attached_pane
        pane.send_keys('^B', enter=False)
        pane.send_keys('d', enter=False)
    """

def tmux_run(*args, **kwargs):
    if len(args) == 1 and callable(args[0]):
        print(f'args: {args}, kwargs: {kwargs}')
        func = args[0]
        
        def inner(*args, **kwargs):
            sig = inspect.signature(func)
            keys = sig.parameters.keys()
            if len(keys) == 1:
                c = args[0]
                
                enterResponder = Responder(
                    pattern=r'\n>',
                    response='\n'
                )
                task_result = c.run(
                    "tmux a -t Fabric",
                    hide=False, pty=True,
                    watchers=[enterResponder]
                )
                
                func_result = func(*args)
            else:
                func_result = func(*args, **kwargs)
            print('===== detach')
            detach(c)
            return func_result
        
        inner.__name__ = func.__name__
        
        return inner
