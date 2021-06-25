#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path
import os


def get_args():
    parser = argparse.ArgumentParser(prog='auto bowtie2', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument("-g", "--genome", required=True, type=str, dest="genome",
                        help="Path to dir containg reference genome")
    parser.add_argument("-t", "--threads", required=False, default=1, type=int, dest="threads",
                        help="Number of threads to use")
    return parser.parse_args()


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def main(args):
    reference_genome = Path(args.genome)

    try:
        os.mkdir(os.getcwd() + '/IndexesGryrodactylus')
    except:
        pass

    output = subprocess.run(["bowtie2-build", str(reference_genome), "IndexesGryrodactylus/Gyrodactylus_index", "--threads", str(args.threads)]
                            , capture_output=True)
    print(output.stdout.decode())


if __name__ == "__main__":
    args = get_args()
    main(args)
