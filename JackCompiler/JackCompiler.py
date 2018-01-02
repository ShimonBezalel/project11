"""
The program receives a name of a file or a directory, and compiles the file,
or all the Jack files in this directory. For each Xxx.jack file, it creates a Xxx.vm
file in the same directory. The logic is
as follows:
For each Xxx.jack file in the directory:
1. Create a tokenizer from the Xxx.jack file
2. Create a VM-writer into the Xxx.vm file
3. Compile(INPUT: tokenizer, OUTPUT: VM-writer)


Include testing modules.


"""

