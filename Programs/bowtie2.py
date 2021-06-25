#!/usr/bin/env python3

import argparse
import itertools
import subprocess
from pathlib import Path
import os


def get_args():
    parser = argparse.ArgumentParser(prog='auto bowtie2', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--dir", required=True, type=str, dest="dir",
                        help="Path to dir containg *.fastq.gz reads")
    parser.add_argument("--g1", "--genome1", required=True, type=str, dest="genome1",
                        help="Path to dir containg reference genome")
    parser.add_argument("--g2", "--genome2", required=True, type=str, dest="genome2",
                        help="Path to dir containg reference genome")
    parser.add_argument("-s", "--save", required=True, type=str, dest="save", help="Path to empty dir used for save")
    parser.add_argument("--se", "--saveend", required=True, type=str, dest="saveend", help="Path to empty dir used for save")
    parser.add_argument("-t", "--threads", required=False, default=1, type=int, dest="threads",
                        help="Number of threads to use")

    return parser.parse_args()


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

lst1 = []
lst2 = []

lst11 = []
lst22 = []

nazwa1 = []
nazwa2 = []

def main(args):
    dir, save, reference_genome1, reference_genome2, saveend = Path(args.dir), Path(args.save), Path(args.genome1), Path(args.genome2), Path(args.saveend)
    if not dir.is_dir():
        raise FileNotFoundError("Given dir is not dir")
    if not save.exists():
        save.mkdir()
    if not saveend.exists():
        saveend.mkdir()
    if len(list(save.iterdir())) > 0:
        raise FileExistsError("Save directory is not empty")

    try:
        os.mkdir(os.getcwd() + '/Indexes')
    except:
        pass

    output = subprocess.run(["bowtie2-build", str(reference_genome1), "Indexes/Genome1_index", "--threads", str(args.threads)]
                            , capture_output=True)
    print(output.stdout.decode())

    output = subprocess.run(
        ["bowtie2-build", str(reference_genome2), "Indexes/Genome2_index", "--threads", str(args.threads)]
        , capture_output=True)
    print(output.stdout.decode())

    for file1, file2 in grouper(2, sorted(list(dir.iterdir()))):
        if not file1 or not file2:
            continue

        lst1.append(file1)
        lst2.append(file2)
        outname = save / Path(file1.stem[:len(file1.stem) - 9] + ".fastq")
        nazwa1.append(outname)
    for i in range(len(lst1)):
        output = subprocess.run(["bowtie2", "-x", "Indexes/Genome1_index", "-1", lst1[i], "-2", lst2[i], "--un-conc",
                                 str(nazwa1[i]), "--threads", str(args.threads)],
                                capture_output=True)

    print(output.stdout.decode())

    for file1 in save.iterdir():
        if not file1:
            continue

        output2 = subprocess.run(["gzip", str(file1)],
                                capture_output=True)
    print(output2.stdout.decode())


    for file1, file2 in grouper(2, sorted(list(save.iterdir()))):
        if not file1 or not file2:
            continue

        lst11.append(file1)
        lst22.append(file2)
        outname2 = saveend / Path(file1.stem[:len(file1.stem) - 8] + ".fastq")
        nazwa2.append(outname2)
    for i in range(len(lst11)):
        output = subprocess.run(["bowtie2", "-x", "Indexes/Genome2_index", "-1", lst11[i], "-2", lst22[i], "--un-conc",
                                 str(nazwa2[i]), "--threads", str(args.threads)],
                                capture_output=True)

    print(output.stdout.decode())

    for file1 in saveend.iterdir():
        if not file1:
            continue

        output2 = subprocess.run(["gzip", str(file1)],
                                capture_output=True)
    print(output2.stdout.decode())


if __name__ == "__main__":
    args = get_args()
    main(args)
