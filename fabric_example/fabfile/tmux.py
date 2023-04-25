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
    #print('=== fabfile.tmux.@tmux_run')
    """print(f'args: {args}' if args else '' +
          ', ' if args and kwargs else '' +
          f', kwargs: {kwargs}' if kwargs else '')"""
    
    if len(args) == 1 and callable(args[0]):
        func = args[0]
        #sig = inspect.signature(func)
        #params = sig.parameters.keys()
        #print(f'params: {params}')
        
        def inner(*args, **kwargs):
            """
            if args and kwargs:
                result = func(*args, **kwargs)
            elif args:
                result = func(*args)
            elif kwargs:
                result = func(**kwargs)
            
            return result
            """
            return func(*args)
        
        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        
        return inner
