"""
Main for Nand to Tetris project7, HUJI

Runs multiple conversions from .vm (virtual machine language) files to .asm
language files.
Authors: Shimon Heimowitz, Karin Sorokin

"""

import sys
import os
import traceback
from JackCompiler import JackCompiler as Compiler
from JackCompiler.SyntaxAnalyzer import Analyzer as Analyzer
FILE_PATH = 1

FILE_EXTENSION_JACK = '.jack'
FILE_EXTENSION_VM = '.vm'
FILE_EXTENSION_XML = '.xml'


def main(path, no_tokenize=True, no_compile=False):
    """
    Main Compiler. Checks legality of arguments and operates on directory
    or file accordingly.
    :param path: argument
    """
    jack_files = []
    if not os.path.exists(path):
        print("Error: File or directory does not exist: %s"
              % path)
        return

    elif os.path.isdir(path):  # Directory of files
        jack_files = filter_paths(path)
        dir_path = path
        if not jack_files:  # no vm files found
            print("Error: No files matching %s found in supplied "
                  "directory: %s" % (FILE_EXTENSION_JACK, path))
            return

    elif os.path.isfile(path):  # Single file
        if not path.endswith(FILE_EXTENSION_JACK):
            print("Error: Mismatched file type.\n\"%s\"suffix is not a valid "
                  "file type. Please supply .jack filename or dir." % path)
            return
        jack_files.append(path)
        dir_path = os.path.dirname(path)


    else:
        print("Error: Unrecognized path: \"%s\"\n"
              "Please supply dir or path/filename.vm")
        return


    # Initilizes write based, using a condition for multiple file reading.
    # Multiple files have a special initialization
    analyzer = Analyzer.Analyzer()
    compiler = Compiler.Compiler()

    for jack_file in jack_files:
        try:
            if not no_tokenize:
                dest_file_name = parse_filename(jack_file, FILE_EXTENSION_XML,
                                                tokenize_only=True)
                analyzer.tokenize(jack_file, dest_file_name)

            if not no_compile:
                dest_file_name = parse_filename(jack_file, FILE_EXTENSION_VM)
                # analyzer.compile(jack_file, dest_file_name)
                compiler.compile(jack_file, dest_file_name)

        except OSError:
            print("Could not open {} as jack file.\n If file exists, check spelling"
                  " of file path.".format(jack_file))


        except Exception as e:
            print("Some exception occurred while parsing {}.".format(jack_file), e)
            traceback.print_exc()



def filter_paths(path):
    """
    Filter vm file paths in case a directory path is supplied
    """
    return ["{}/{}".format(path, f) for f in os.listdir(path) if
            f.endswith(FILE_EXTENSION_JACK)]


def parse_filename(path, extension, tokenize_only=False):
    """
    Convert file name to .xml suffix
    :param path:
    :return:
    """
    stripped_path = os.path.splitext(path)[0]

    if tokenize_only:
        stripped_path += "T"

    return stripped_path + extension



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Wrong number of arguments.\n"
              "Usage: JackCompiler file_name.jack or /existing_dir_path/")
    else:
        main(sys.argv[FILE_PATH], no_compile=False, no_tokenize=True)
