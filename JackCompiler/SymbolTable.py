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
    variable declared in a "var" statement) or used
    """

from enum import Enum
TYPE        = 0
KIND        = 1
NUM         = 2

# kinds = ["local", "argument", "static", "field", "class", "subroutine"]
kinds = ["local", "argument", "static", "field"]


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

        self.class_table = self.Class_Table()
        self.subroutine_tables = [self.Subroutine_Table()]

        # self.retrieved = None

    def start_subroutine(self):
        """
        Starts a new subroutine scope (i.e. erases all names in the previous subroutine’s
        scope.)
        :return:
        """
        self.subroutine_tables[0] = self.Subroutine_Table()
        # self.subroutine_tables.append(self.Subroutine_Table())

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
        if kind in ["static", "field"]:
            assert name not in self.class_table.table.keys()
            num = self.class_table.counters[kind]
            self.class_table.counters[kind] += 1
            self.class_table.table[name] = [type, kind, num]
        elif kind in ["argument", "local"]:
            assert name not in self.subroutine_tables[-1].table.keys()
            num = self.subroutine_tables[-1].counters[kind]
            self.subroutine_tables[-1].counters[kind] += 1
            self.subroutine_tables[-1].table[name] = [type, kind, num]
        else:
            raise ValueError("'{}' is an unrecognized type to define in the symbol "
                             "table".format(kind))

    def var_count(self, kind):
        """
        Returns the number of variables of the given kind already defined in the current
        scope.
        :param kind: one of [static, field, argument, var]
        :return: an int representing cur count
        """
        if kind in ["static", "field"]:
            return self.class_table.counters[kind]
        if kind in ["argument", "local"]:
            return self.subroutine_tables[-1].counters[kind]

        else:
            raise ValueError("{} is an unrecognized type to define in the symbol "
                             "table".format(kind))

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in
        the current scope. Returns NONE if the
        identifier is unknown in the current scope.
        :param name: string of symbol identifier
        :return:
        """
        if name in self.subroutine_tables[-1].table.keys():
            return self.subroutine_tables[-1].table[name][KIND]

        elif name in self.class_table.table.keys():
            return self.class_table.table[name][KIND]

        else:
            return None


    def type_of(self, name):
        """
        Returns the type of the named identifier in
        the current scope.
        :param name: string of symbol identifier
        :return:
        """
        if name in self.subroutine_tables[-1].table.keys():
            return self.subroutine_tables[-1].table[name][TYPE]

        elif name in self.class_table.table.keys():
            return self.class_table.table[name][TYPE]

        else:
            return None

    def index_of(self, name):
        """
        Returns the index assigned to named
        identifier.
        :param name: string of symbol identifier
        :return:
        """
        if name in self.subroutine_tables[-1].table.keys():
            return self.subroutine_tables[-1].table[name][NUM]

        elif name in self.class_table.table.keys():
            return self.class_table.table[name][NUM]

        else:
            return None


    # ------------------ Internal/ alternative API   ------------------------------------
    class Subroutine_Table:
        """

        """
        def __init__(self):
            """

            """
            self.counters = {kind: 0 for kind in kinds}
            self.table = {}


    class Class_Table:
        """

        """
        def __init__(self):
            """

            """
            self.counters = {kind: 0 for kind in kinds}
            self.table = {}

    # def in_table(self, name):
    #     """
    #     Searches for a specific named symbol in the table, working its way up the scopes
    #     :param name:
    #     :return:
    #     """
    #     self.retrieved = None
    #     found = name in self.class_table.keys()
    #     if found:
    #         self.retrieved = self.class_table[name]
    #     elif self.parent_scope:
    #         found = self.parent_scope.in_table(name)
    #         self.retrieved = self.parent_scope._retrieve()
    #     return found
    #
    # def _retrieve(self):
    #     """
    #     Should only be called after in_table, and returned true. Returns the the relevant
    #     information of a
    #      given symbol name
    #     :return:
    #     """
    #     assert self.retrieved
    #     return self.retrieved
    #
    # def get_number(self, name):
    #     """
    #     Returns the number of the specific name in the table. If the
    #     name is not in the table, returns -1
    #     :param name:
    #     :return:
    #     """
    #     if self.in_table(name):
    #         assert self.retrieved[KIND] in kinds[:INDEX_CATAGORIES]
    #         return self.retrieved[NUM]
    #     else:
    #         return -1
    #
    # def get_catagory(self, name):
    #     """
    #     Returns the kind of the specific name in the table. If the
    #     name is not in the table or it's parent scopes, returns None
    #     :param name:
    #     :return:
    #     """
    #     if self.in_table(name):
    #         return self.retrieved[KIND]
    #     else:
    #         return None
    #
    # def get_type(self, name):
    #     """
    #     Returns the number of the specific name in the table. If the
    #     name is not in the table or it's parent scopes, returns None
    #     :param name:
    #     :return:
    #     """
    #     if self.in_table(name):
    #
    #         return self.retrieved[TYPE]
    #     else:
    #         return None
    #
    #
    # def add_symbol(self, name, type, kind):
    #     """
    #     Adds a new symbol into the table. Symbol assumed not to exist in current scope
    #     :param name:
    #     :param type:
    #     :param kind:
    #     :return:
    #     """
    #
    #     # We may want to add the statics into the heighest scope or something
    #
    #     assert name not in self.class_table.keys()
    #     if kind in self.counters.keys():
    #         num = self.counters[kind]
    #         self.counters[kind] += 1
    #     else:
    #         raise ValueError("Unrecognized kind {}".format(kind))
    #     # np.append(self.table, [name, type, kind, num])
    #     self.class_table[name] = [type, kind, num]
    #
    # def _clean_non_static(self):
    #     """
    #     Erases all entries in this table except the static values
    #     :return:
    #     """
    #     self.class_table = {k: v for k, v in self.class_table.items() if "static" == v[TYPE]}
    #
    # def kill_scope(self):
    #     """
    #     kills current scope, by saving all the statics and destorying the current layer.
    #     :return:
    #     """
    #     self._clean_non_static()
    #     self.parent_scope._add_statics(self.class_table)
    #
    # def _add_statics(self, statics):
    #     self.class_table.update(statics)








