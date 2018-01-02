"""
A designated module for translating parsed jack code into vm-language code.
"""


class CodeGenerator():
    """

    """

    def write_expression(self, expression):
        """
        recursive function for write an expression in vm
        The write_expression(exp) algorithm:
        if exp is a constant n then output "push n"
        if exp is a variable v then output "push v"
        if exp is op(exp1) then codeWrite(exp1); output "op";
        if exp is (exp1 op exp2) then codeWrite(exp1); codeWrite(exp2); output "op";
        if exp is f (exp1, ..., expn) then codeWrite(exp1); ... codeWrite(exp1); output "call f";
        :param expression:
        :return:
        """
        pass


    def write_flow(self):
        """
        write
        :return:
        """
        # This will probably be broken up into smaller bits
        pass