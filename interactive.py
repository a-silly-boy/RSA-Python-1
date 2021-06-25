import commands


while True:
    args = input('> ').split(' ')
    commands.execute(args[0], *args[1:])
