"""The compiler's symbol table module.

 This module provides services for creating, populating, and using a symbol table. Recall that
each symbol has a scope from which it is visible in the source code. In the symbol table, each
symbol is given a running number (index) within the scope, where the index starts at 0 and is
reset when starting a new scope. The following kinds of identifiers may appear in the symbol
table:
    Static:     Scope: class.
    Field:      Scope: class.
    Argument:   Scope: subroutine (method/function/constructor).
    Var:        Scope: subroutine (method/function/constructor).

When compiling code, any identifier not found in the symbol table may be assumed to be a
subroutine name or a class name. Since the Jack language syntax rules suffice for distinguishing
between these two possibilities, and since no “linking” needs to be done by the compiler, these
identifiers do not have to be kept in the symbol table.


 It is used to extend the syntax analyzer built
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
TYPE        = 0
KIND        = 1
NUM         = 2

# INDEX_CATAGORIES = 4

# kinds = ["var", "argument", "static", "field", "class", "subroutine"]
kinds = ["var", "argument", "static", "field"]

class Table_Scopes(Enum):
    class_scope     = "class"
    method_scope    = "method"

class SymbolTable:
    """

    """

    # ------------------ Suggested API   ------------------------------------

    def __init__(self):
        """
        Generate a new level of the table, by creating a new scope. The parent's scope
        must be sent in the constructor. Only the highest scope should be none.
        :param  parent_scope:
        """
        # self.parent_scope = parent_scope

        # Comment: you will probably need to use two separate hash tables to implement the symbol
        # table: one for the class-scope and another one for the subroutine-scope. When a new subroutine
        # is started, the subroutine-scope table should be cleared.

        self.class_table = {}
        self.class_counters = {kind: 0 for kind in kinds}
        self.subroutine_table = {}
        self.subroutine_counters = {kind: 0 for kind in kinds}
        # self.counters = {
        #     "local"     : 0,
        #     "argument"  : 0,
        #     "var"       : 0,
        #     "static"    : 0,
        #     "field"     : 0,
        #     "class"     : 0,
        #     "subroutine": 0
        # }
        self.retrieved = None

    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s
        scope.)
        :return:
        """
        self.subroutine_table

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running
        index. STATIC and FIELD identifiers have a class scope, while ARG and VAR
        identifiers have a subroutine scope.
        :param name: unique identifier representing this symbol (string)
        :param type: type of identifier
        :param kind: one of [static, field, argument, var]
        :return:
        """
        pass

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current
        scope.
        :param kind: one of [static, field, argument, var]
        :return: an int representing cur count
        """
        return self.counters[kind]

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope.
        :param name: string of symbol identifier
        :return:
        """
        if self.in_table(name):
            return self.retrieved[KIND]
        else:
            return None

    def type_of(self, name):
        """
        Returns the type of the named identifier in
        the current scope.
        :param name: string of symbol identifier
        :return:
        """
        if self.in_table(name):

            return self.retrieved[TYPE]
        else:
            return None

    def index_of(self, name):
        """
        Returns the index assigned to named
        identifier.
        :param name: string of symbol identifier
        :return:
        """
        if self.in_table(name):
            assert self.retrieved[KIND] in kinds[:INDEX_CATAGORIES]
            return self.retrieved[NUM]
        else:
            return -1


    # ------------------ Internal/ alternative API   ------------------------------------
    def in_table(self, name):
        """
        Searches for a specific named symbol in the table, working its way up the scopes
        :param name:
        :return:
        """
        self.retrieved = None
        found = name in self.class_table.keys()
        if found:
            self.retrieved = self.class_table[name]
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
            assert self.retrieved[KIND] in kinds[:INDEX_CATAGORIES]
            return self.retrieved[NUM]
        else:
            return -1

    def get_catagory(self, name):
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

        assert name not in self.class_table.keys()
        if kind in self.counters.keys():
            num = self.counters[kind]
            self.counters[kind] += 1
        else:
            raise ValueError("Unrecognized kind {}".format(kind))
        # np.append(self.table, [name, type, kind, num])
        self.class_table[name] = [type, kind, num]

    def _clean_non_static(self):
        """
        Erases all entries in this table except the static values
        :return:
        """
        self.class_table = {k: v for k, v in self.class_table.items() if "static" == v[TYPE]}

    def kill_scope(self):
        """
        kills current scope, by saving all the statics and destorying the current layer.
        :return:
        """
        self._clean_non_static()
        self.parent_scope._add_statics(self.class_table)

    def _add_statics(self, statics):
        self.class_table.update(statics)





