# This script is meant to be executed as a CLI tool and may assist in generating graph datasets

from sys import argv

def print_help():
    print(f"""     Use: {argv[0]} OPTIONS \n
        Options:
        --parser -p <format> : Sets the format the parser should use to read the file
        --output -o <path> : Output to specified path
          
    When using definition files, the parameters set through arguments overwrite their counterparts in the definition files.""")
