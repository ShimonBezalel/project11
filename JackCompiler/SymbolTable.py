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
    def __init__(self, parent_scope=None):
        """
        Generate a new level of the table, by creating a new scope. The parent's scope
        must be sent in the constructor. Only the highest scope should be none.
        :param  parent_scope:
        """
        self.parent_scope = parent_scope
        self.table = {}
        self.counters = {
            "local"     : 0,
            "argument"  : 0,
            "var"       : 0,
            "static"    : 0,
            "field"     : 0
        }
        self.retrieved = None

    def in_table(self, name):
        """
        Searches for a specific named symbol in the table, working its way up the scopes
        :param name:
        :return:
        """
        self.retrieved = None
        found = name in self.table.keys()
        if found:
            self.retrieved = self.table[name]
        elif self.parent_scope:
            found = self.parent_scope.in_table(name)
            self.retrieved = self.parent_scope._retrieve()
        return found

    def _retrieve(self):
        """
        Should only be called after in_table, and returned true. Returns the the relevant
        information of a
         given symbol name
        :return:
        """
        assert self.retrieved
        return self.retrieved

    def get_number(self, name):
        """
        Returns the number of the specific name in the table. If the
        name is not in the table, returns -1
        :param name:
        :return:
        """
        if self.in_table(name):
            return self.retrieved[NUM]
        else:
            return -1

    def get_kind(self, name):
        """
        Returns the kind of the specific name in the table. If the
        name is not in the table or it's parent scopes, returns None
        :param name:
        :return:
        """
        if self.in_table(name):
            return self.retrieved[KIND]
        else:
            return None

    def get_type(self, name):
        """
        Returns the number of the specific name in the table. If the
        name is not in the table or it's parent scopes, returns None
        :param name:
        :return:
        """
        if self.in_table(name):
            return self.retrieved[TYPE]
        else:
            return None


    def add_symbol(self, name, type, kind):
        """
        Adds a new symbol into the table. Symbol assumed not to exist in current scope
        :param name:
        :param type:
        :param kind:
        :return:
        """

        # We may want to add the statics into the heighest scope or something

        assert name not in self.table.keys()
        if kind in self.counters.keys():
            num = self.counters[kind]
            self.counters[kind] += 1
        else:
            raise ValueError("Unrecognized kind {}".format(kind))
        # np.append(self.table, [name, type, kind, num])
        self.table[name] = [type, kind, num]

    def _clean_non_static(self):
        """
        Erases all entries in this table except the static values
        :return:
        """
        self.table = {k: v for k, v in self.table.items() if "static" == v[TYPE]}

    def kill_scope(self):
        """
        kills current scope, by saving all the statics and destorying the current layer.
        :return:
        """
        self._clean_non_static()
        self.parent_scope._add_statics(self.table)

    def _add_statics(self, statics):
        self.table.update(statics)





