"""The compiler's symbol table module. It is used to extend the syntax analyzer built
in project 10. This module sotres and handles the following data:
-> The identifier's name, as done by the current version of the syntax analyzer.
-> The identifier's category: var, argument, static, field, class, or subroutine.
-> If the identifier's category is var, argument, static, or field, the running index
    assigned to the identifier by the symbol table.
-> Whether the identifier is presently being defined (e.g. the identifier stands for a
    variable declared in a "var" statement) or used."""

# import numpy as np

# NAME = 0
from enum import Enum
TYPE = 0
KIND = 1
NUM  = 2

class Table_Scopes(Enum):
    class_scope     = "class"
    method_scope    = "method"

class SymbolTable:
    """

    """
    def __init__(self, table_scope):
        """

        :param table_typle:
        """
        self.scope = table_scope
        self.table = {}
        self.counters = {
            "argument"  : 0,
            "var"       : 0,
            "static"    : 0,
            "field"     : 0
        }

    def in_table(self, name):
        """
        Searches for a specific named symbol in the table
        :param name:
        :return:
        """
        return name in self.table.keys()

    def get_number(self, name):
        """
        Returns the number of the specific name in the table. If the
        name is not in the table, returns -1
        :param name:
        :return:
        """
        try:
           num = self.table[name][NUM]
           return num
        except KeyError:
            return -1

    def add_symbol(self, name, type, kind):
        assert name not in self.table.keys()
        if kind in self.counters.keys():
            num = self.counters[kind]
            self.counters[kind] += 1
        else:
            raise ValueError("Unrecognized kind {}".format(kind))
        # np.append(self.table, [name, type, kind, num])
        self.table[name] = [type, kind, num]

    def clean_non_static(self):
        """
        Erases all entries in this table except the static values
        :return:
        """
        self.table = {k: v for k, v in self.table.items() if "static" == v[TYPE]}




