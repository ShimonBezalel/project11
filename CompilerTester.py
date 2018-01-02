"""
For each test program, the following routines are operated:

-> Compiling the program directory using this compiler. This action compiles all
    the .jack files in the directory into corresponding .vm files;
-> Inspection of the generated .vm files. If there are any visible problems, the
    compiler must be fixed, then go to step 1 ;
-> Testing the translated VM program by loading the program directory into the
    supplied VM emulator; If the test program behaves unexpectedly or some error
    message is displayed by the VM emulator, the compiler is fixed and go to to step 1.
"""