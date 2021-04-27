import sys
import hedy

def printHelp():
    print("Usage: python hedy.py [--help] <filename> [--level <level (1-8)>]\n\nTo specify a level, add #level <level> to the top of your file or use the --level <level> argument.")
    sys.exit(1)

def print(uitvoer):
    sys.stdout.write(uitvoer + '\n')

def main():
    # python3 hedy.py <filename(0)> [levelargument(1)] [level(2)]

    args = sys.argv[1:]
    args_length = len(args)

    if args_length == 0 or args[0] == "-h" or args[0] == "--help":
        printHelp()

    level = 0 # Set level to 0 by default so we can check later if the level already has been set
    filename = args[0] # Set filename to args[0]

    if not args_length == 1:
        if args_length == 3:
            if args[1] == "--level" or args[1] == "-l":
                try:
                    level = int(args[2])
                    if level > 8:
                        print("Level has been set to 8, because the value specified was to high")
                        level = 8
                except ValueError:
                    print("Level argument is not an integer, skipping argument.")

    lines = ""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if level == 0:
        if lines[0].lower().startswith('#level'):
            parts = lines[0].split(' ')
            if len(parts) >= 2:
                level = int(parts[1])
                if level > 8:
                    print("Level has been set to 8, because the value specified was to high")
                    level = 8

    program = '\n'.join([line
        for line in lines
        if not line.startswith('#')])

    try:
        hedy.execute(program, level)
    except hedy.HedyException as e:
        sys.stderr.write('An error occurred: %s\n' % e.error_code)
        sys.stderr.write('Error attributes:\n')
        for key, value in e.arguments.items():
            sys.stderr.write(f'{key}={value}\n')
        sys.exit(1)

if __name__ == '__main__':
    main()
