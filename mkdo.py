
r'''install a python module command in the bin directory
'''

import argparse
import sys, os
from os.path import basename, dirname, splitext, join, exists, isdir, islink
import subprocess

this_name = splitext(basename(__file__))[0]

def mkdo(name:str, bin_dir:str=None):
    bin_dir = bin_dir or dirname(subprocess.check_output(['which', this_name]).decode())
    bin_name = join(bin_dir, name)

    if name=='.wrapper':
        for fname in os.listdir(bin_dir):
            if fname=='.wrapper':
                continue

            if islink(join(bin_dir, fname)):
                if basename(os.readlink(join(bin_dir, fname))) == '.wrapper':
                    print(mkdo(fname, bin_dir))

            else:
                if os.stat(join(bin_dir, fname)).st_size < 34:
                    # update to python3s instead of python
                    with open(join(bin_dir, fname)) as f:
                        s = f.read()
                    if s.startswith('python3 -m `basename "$0"` $@'):
                        print(mkdo(fname, bin_dir))
    else:

        if exists(bin_name):
            os.unlink(bin_name)

        src = 'python3s -m `basename "$0"` $@\n'

        with open(bin_name, 'w') as f:
            f.write(src)

        os.chmod(bin_name, 0o755)

        return bin_name

def main():
    parser = argparse.ArgumentParser(prog=this_name, description=__doc__)
    parser.add_argument('name', help='command name (python module name) or .wrapper to convert wrappers')
    parser.add_argument('-d', help=f'bin directory (default=location of {this_name} command)')

    args = parser.parse_args()

    try:
        r = mkdo(args.name, args.d)
        print (r)
    except Exception as e: # Best if replaced with explicit exception
        print (e, file=sys.stderr)
        exit(1)

if __name__=='__main__':
    main()

