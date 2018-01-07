"""
This class writes VM commands into a file. It encapsulates the VM command syntax.

Emits VM commands into a file
"""

ARITHMETIC_COMMANDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
SEGMENTS =  ["const", "arg", "local", "static", "this", "that", "pointer", "temp"]

NEW_LINE = "\n"

class VMWriter:
    def __init__(self, outfile):
        """
        Creates a new file and prepares it for writing
        VM commands
        :param outfile: output file/stream
        """
        self.file = open(outfile, 'w')


    def write_push(self, segment, index):
        """
        Writes a VM push command
        :param segment: one of (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
        :param index: int
        :return:
        """
        self.file.write("push " + segment + " " + str(index) + NEW_LINE)


    def write_pop (self, segment, index):
        """
        Writes a VM pop command
        :param segment: one of (CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP)
        :param index: int
        :return:
        """
        self.file.write("pop " + segment + " " + str(index) + NEW_LINE)

    def write_arithmetic(self, command):
        """
        Writes a VM arithmetic command
        :param command: one of  (ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT)
        :return:
        """
        assert command in ARITHMETIC_COMMANDS
        self.file.write(command.lower() + NEW_LINE)

    def write_label(self, label):
        """
        Write a VM label command
        :param label: a string
        :return:
        """
        self.file.write("label " + label + NEW_LINE)

    def write_goto(self, label):
        """
        Write a VM goto command
        :param label: a string
        :return:
        """
        self.file.write("goto " + label + NEW_LINE)

    def write_if(self, label):
        """
        Write a VM if command
        :param label: a string
        :return:
        """
        # todo: if-goto in this case?
        self.file.write("if-goto " + label + NEW_LINE)

    def write_call(self, name, num_args):
        """
        write call command
        :param name: string
        :param num_args: int
        :return:
        """
        self.file.write("call " + name + " " + str(num_args) + NEW_LINE)

    def write_function(self, name, num_locals):
        """
        write a function command
        :param name:
        :param num_locals:
        :return:
        """

        self.file.write("function " + name + " " + str(num_locals) + NEW_LINE)

    def write_return(self):
        """
        write a return command
        :return:
        """
        self.file.write("return" + NEW_LINE)


    def close(self):
        """
        close the file
        :return:
        """
        self.file.close()