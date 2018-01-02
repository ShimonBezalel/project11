"""
A designated module for translating parsed jack code into vm-language code.

For each test program, the following routines are operated:
-> Compiling the program directory using this compiler. This action compiles all
    the .jack files in the directory into corresponding .vm files;
-> Inspection of the generated .vm files. If there are any visible problems, fix your
compiler
    and go to step 1 (remember: all the supplied test programs are error-free);
Test the translated VM program by loading the program directory into the supplied VM emulator and executing it using the "no animation" mode. Each one of the six test programs contains specific execution guidelines, as listed below; test the program according to these guidelines;
If the test program behaves unexpectedly or some error message is displayed by the VM emulator, fix your compiler and go to to step 1.
"""