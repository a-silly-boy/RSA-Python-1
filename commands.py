from types import FunctionType

import core


COMMAND_NOT_FOUND = 'command_not_found'


def safe(func: FunctionType) -> FunctionType:
    '''A function decorator reports all the errors'''

    def new_func(*args):
        try:
            func(*args)
        except:
            print('{}: an error had occurred'.format(func.__name__))
    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    return new_func


@safe
def command_not_found(command: str, *rest: tuple) -> None:
    '''Shows an 'command not found' message'''

    print('{}: command not found'.format(command))


# @safe
def quit(*rest: tuple) -> None:
    '''Exits the program'''

    exit()


@safe
def help(command: str = None, *rest: tuple) -> None:
    '''Shows the info of <commmand>'''

    if command == None:
        for func in public_table.values():
            print('{}: {}'.format(func.__name__, func.__doc__ if func.__doc__ != None else 'No info'))
            pass
        return

    func = public_table[command]
    if func.__doc__ == None:
        print('No info')
        return

    print(func.__name__, end=' ')
    for item in func.__doc__.split(' '):
        if item.startswith('<') and item.endswith('>'):
            print(item, end=' ')
    print('\b:\n\t' + func.__doc__)


keys = {}


@safe
def start(id: str, *rest: tuple) -> None:
    '''Starts a new RSA encrypt/decrypt session called <id>'''

    global keys
    keys[id] = core.gen_keys()
    print('{} started'.format(id))


@safe
def info(id: str, *rest: tuple) -> None:
    '''Shows the info of session <id>'''

    global keys
    print('n = {}\ne = {}\nd = {}'.format(
        keys[id]['n'], keys[id]['e'], keys[id]['d']))


@safe
def encrypt(id: str, plaintext: int, *rest: tuple) -> None:
    '''Encrypts the <plaintext> with the keys in <id>'''

    global keys
    print(core.encrypt(int(plaintext), keys[id]['e'], keys[id]['n']))


@safe
def decrypt(id: str, ciphertext: int, *rest: tuple) -> None:
    '''Decrypt the <plaintext> with the keys in <id>'''

    global keys
    print(core.decrypt(int(ciphertext), keys[id]['d'], keys[id]['n']))


@safe
def end(id: str, *rest: tuple) -> None:
    '''Ends session <id>'''

    global keys
    del keys[id]
    print('{} ended'.format(id))


public_table = {'quit': quit,
         'help': help,
         'start': start,
         'info': info,
         'encrypt': encrypt,
         'decrypt': decrypt,
         'end': end}

private_table = {'command_not_found': command_not_found}


def execute(name, *args):
    if not public_table.get(name):
        private_table[COMMAND_NOT_FOUND](name)
    else:
        public_table[name](*args)
