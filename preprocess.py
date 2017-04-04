""" Concatenate all tune files into a single txt for torch training. """

import os
import json

def clean_abc(abc):
    """ Remove blacklisted lines from ABC """
    return "\n".join([line for line in abc.split("\n") if not (
        line == "" or
        line.startswith("A:") or
        line.startswith("B:") or
        line.startswith("C:") or
        line.startswith("D:") or
        line.startswith("F:") or
        line.startswith("G:") or
        line.startswith("H:") or
        line.startswith("I:") or
        line.startswith("m:") or
        line.startswith("N:") or
        line.startswith("O:") or
        line.startswith("r:") or
        line.startswith("S:") or
        line.startswith("s:") or
        line.startswith("W:") or
        line.startswith("w:") or
        line.startswith("X:") or
        line.startswith("Z:")
    )])


def copy_abc_to_target(tune_file, target, abc_condition):
    """ Write abc from tune file to the end of the target """
    tune_json = json.load(tune_file)
    for tune in tune_json:
        if abc_condition(tune["abc"]):
            target.write(clean_abc(tune["abc"]))
            target.write("\n\n")

def all_tunes_condition(_):
    """ The condition that accepts all tunes """
    return True

def common_and_cut_time_condition(abc):
    """ All tunes in common or cut time """
    return (("M:4/4" in abc) or
            ("M:2/2" in abc) or
            ("M: 4/4" in abc) or
            ("M: 2/2" in abc) or
            ("M:C" in abc) or
            ("M: C" in abc))

def reels_condition(abc):
    """ All tunes in common or cut time """
    return "Reel" in abc

def main():
    """ The main executable """
    tune_file_directory = "tune-files"
    output_file = "all-abcs.txt"

    with open(output_file, 'a') as outfile:
        for filename in os.listdir(tune_file_directory):
            with open(os.path.join(tune_file_directory, filename)) as tune_file:
                copy_abc_to_target(tune_file, outfile, all_tunes_condition)


if __name__ == '__main__':
    main()
