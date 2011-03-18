import sys

from pyOrcaFile import get_livetime

def main(args):
    fname = args[0]
    try:
        handle = open(fname)
        print(get_livetime(handle))
    except Exeption as e:
        print(e)

if __name__ == "__main__":
    main(sys.argv[1:])
