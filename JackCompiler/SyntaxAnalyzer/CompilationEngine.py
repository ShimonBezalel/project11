"""
This class does the compilation itself. It reads its input from a JackTokenizer and writes its
output into a VMWriter. It is organized as a series of compilexxx() methods, where xxx is a
syntactic element of the Jack language. The contract between these methods is that each
compilexxx() method should read the syntactic construct xxx from the input, advance() the
tokenizer exactly beyond xxx, and emit to the output VM code effecting the semantics of xxx.
Thus compilexxx() may only be called if indeed xxx is the next syntactic element of the input.
If xxx is a part of an expression and thus has a value, then the emitted code should compute this
value and leave it at the top of the VM stack.
"""

from JackCompiler.SyntaxAnalyzer.JackTokenizer import JackTokenizer, Token_Types
from JackCompiler import VMWriter
from JackCompiler.SymbolTable import *
from enum import Enum, unique

END_LINE    = "\n"
SPACE         = "  "

# EXPRESSIONS = {"INT_CONST": "integerConstant",
#                 "STRING_CONST": "stringConstant",
#                 "KEYWORD": "KeywordConstant",
#                 "IDENTIFIER": "identifier"}
STATEMENTS      = ['let', 'if', 'while', 'do', 'return']
KEY_TERMS       = ["true", "false", "null", "this"]
# SPECIAL_SYMBOL  = {'&quot;': "\"", '&amp;': "&", '&lt;': "<", '&gt;': ">"}
OPERANDS        = ['+', '-', '*', '&amp;', '|', '&lt;', '&gt;', '=', "/"]
ROUTINES        = ['function', 'method', 'constructor']
ARGS = 'argument'
LOCAL = 'local'
THIS = 'this'
CONSTANT = "CONST"
POINTER = "POINTER"


IF = 0
WHILE = 1


@unique
class BuiltinFunctions(Enum):
    """

    """
    str_new = "String.new"
    str_app_char = "String.appendChar"
    math_div = "Math.divide"
    math_mult = "Math.multiply"
    mem_alloc = "Memory.alloc"





class CompilationEngine():
    """

    """

    def __init__(self, input_file, output_file):
        """
        Creates a new compilation engine with the given input and output. The next
        routine called must be compile_class()
        :param input_file:
        :param output_file:
        """
        self.symbol_table = SymbolTable()
        self.tokenizer = JackTokenizer(input_file)


        # todo: Here we need to see if we open a new writer per class.

        self.writer = VMWriter.VMWriter(output_file)
        self.__reset_label_counter()
        self.num_spaces = 0
        self.buffer = ""
        self.symbol_table = SymbolTable()
        # with open(output_file, 'w') as self.output:
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            # assert self.tokenizer.token_type() == Token_Types.keyword
            if self.tokenizer.keyWord() == 'class':
                self.class_name = None
                self.compile_class()
            else:
                raise KeyError("Received a token that does not fit the beginning of a "
                               "module. " + self.tokenizer.keyWord()
                               + " in " + input_file)
        self.writer.close()

    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """


        # self.write('class', delim=True)
        # self.num_spaces += 1
        # self.write_terminal(self.tokenizer.token_type().value, self.tokenizer.keyWord())
        self.eat('class')
        self.symbol_table = SymbolTable()

        t_type, self.class_name = self.tokenizer.token_type(), self.tokenizer.identifier()
        # self.write_terminal(t_type.value, class_name)

        self.tokenizer.advance()

        # t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
        # self.write_terminal(t_type.value, symbol)
        self.eat('{')

        t_type = self.tokenizer.token_type()
        while t_type != Token_Types.symbol:
            operation = self.tokenizer.keyWord()
            if operation in ['static', 'field']:
                self.compile_class_var_dec()
            elif operation in ROUTINES:
                self.compile_subroutine()
            else:
                raise KeyError("Found statement that does not fit class declaration. ",
                               operation)

            # self.tokenizer.advance()

            t_type = self.tokenizer.token_type()

        # todo: do i need here - self.eat('}')

        # self.write_terminal(t_type.value, self.tokenizer.symbol())
        # self.num_spaces -= 1
        # self.write('class', delim=True, end=True)

    def eat(self, string):
        """
        If the given string is the same as current token (only if it keyword or symbol) the
        tokenizer of the object will be advanced, otherwise an exception will be raised.
        :param string: the expected string.
        :raise: the current token is not the expected string.
        """
        type = self.tokenizer.token_type()
        value = "not keyword and not symbol"
        if type == Token_Types.keyword:
            value = self.tokenizer.keyWord()
        elif type == Token_Types.symbol:
            value = self.tokenizer.symbol()

        if value != string:
            raise Exception("Received '" + value +
                            "' which is not the expected string: '" + string + "'")
        # assert value == string
        self.tokenizer.advance()

    def compile_class_var_dec(self):
        """
        Compiles a static declaration or a field declaration.
        """
        # self.write("classVarDec", True)
        # self.num_spaces += 1

        # First word is static or field.

        # should i check before if i can get a keyword?
        var_kind = self.tokenizer.keyWord()
        if var_kind not in ["static", "field"]:
            raise Exception("Cant compile class variable declaration without static of "
                            "field." + var_kind)
        # self.write("<keyword> " + var_sort + " </keyword>")
        self.tokenizer.advance()

        # Second word is type.
        if self.tokenizer.token_type() == Token_Types.keyword:
            var_type = self.tokenizer.keyWord()
            if var_type not in ["int", "char", "boolean"]:
                raise Exception("Cant compile class variable declaration with invalid "
                                "keyword type." + var_type)
            # self.write("<keyword> " + var_type + " </keyword>")

        elif self.tokenizer.token_type() == Token_Types.identifier:
            # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
            var_type = self.tokenizer.identifier()
        else:
            raise Exception("Cant compile class variable declaration with invalid identifier type.")

        self.tokenizer.advance()

        # Third and so on, are variables names.
        # if self.tokenizer.token_type() != Token_Types.identifier:
        #     raise Exception("Cant compile class variable declaration without varName identifier.")

        # assert self.tokenizer.token_type() == Token_Types.identifier
        # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        var_name = self.tokenizer.identifier()

        self.tokenizer.advance()

        self.symbol_table.define(var_name, var_type, var_kind)
        self.possible_varName(var_type, var_kind)

        # It will always end with ';'
        self.eat(';')
        # self.write("<symbol> ; </symbol>")

        # self.num_spaces -= 1
        # self.write("classVarDec", True, True)

    def possible_varName(self, var_type, var_kind):
        """
        Compile 0 or more variable names, after an existing variable name.
        """
        try:
            self.eat(',')
        except:
            # There is no varName
            return
        # There is a varName
        # self.write("<symbol> , </symbol>")
        # if self.tokenizer.token_type() != Token_Types.identifier:
        #     raise Exception("Cant compile (class or not) variable declaration without varName" +
        #                     " identifier after ',' .")

        # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.symbol_table.define(self.tokenizer.identifier(), var_type, var_kind)
        self.tokenizer.advance()
        self.possible_varName(var_type, var_kind)

# Subroutine Compilation logic ---------------------------------------------------------

    def compile_subroutine(self):
        """
        Compiles a complete method, function or constructor
        :return:
        """

        self.symbol_table.start_subroutine()

        subroutine_type = self.tokenizer.keyWord()

        # Read opening line of function up to parameter list and compile accordingly
        if subroutine_type == "constructor":
            self.compile_constructor()
        elif subroutine_type == "method":
            self.compile_method()
        elif subroutine_type == "function":
            self.compile_function()

        self.eat('(')

        self.compile_param_list()

        self.eat(')')

        self.eat('{')

        # Including return
        self.compile_subroutine_body()

        self.eat('}')

    def compile_constructor(self):
        """
        dedicated function for compiling a contructor only
        :return:
        """
        self.eat("constructor")

        # Compile function signature

        # make sure the constructor func returns a class instance
        assert self.tokenizer.identifier() == self.class_name

        self.cur_func_type = self.class_name

        self.tokenizer.advance()
        self.eat("new")

        func_name = self.class_name + ".new"

        self.writer.write_label(func_name)

        self.writer.write_push(CONSTANT, self.symbol_table.var_count("field"))
        self.writer.write_call(BuiltinFunctions.mem_alloc.value, num_args=1)
        self.writer.write_pop(POINTER, 0)


    def compile_method(self):
        """

        :return:
        """
        self.eat("method")
        self.compile_func_signature()
        self.symbol_table.define("this", self.class_name, "argument")
        self.writer.write_push(ARGS, 0)
        self.writer.write_pop(POINTER, 0)


    def compile_function(self):
        """

        :return:
        """
        self.eat('function')
        self.compile_func_signature()

    def compile_func_signature(self):
        """

        :return:
        """
        t_type = self.tokenizer.token_type()
        if t_type == Token_Types.keyword:
            self.cur_func_type = self.tokenizer.keyWord()
        else:
            self.cur_func_type = self.tokenizer.identifier()

        self.tokenizer.advance()

        func_name = self.class_name + "." + self.tokenizer.identifier()
        self.writer.write_label(func_name)

        self.tokenizer.advance()

    def compile_subroutine_body(self):
        """

        :return:
        """
        t_type = self.tokenizer.token_type()
        while t_type != Token_Types.symbol:
            token = self.tokenizer.keyWord()
            if token == 'var':
                self.compile_var_dec()
            elif token in STATEMENTS:
                # Direct control over return case. This may be unnecessary
                if token == "return":
                    self.compile_return()
                else:
                    self.compile_statements()
            else:
                raise KeyError("an unknown step inside a subroutine, ", t_type)
            # self.tokenizer.advance()
            t_type = self.tokenizer.token_type()

    def compile_param_list(self):
        """
        Compiles a parameter list, which may be empty, not including the "()"
        :return:
        """
        t_type = self.tokenizer.token_type()
        finished = t_type == Token_Types.symbol and self.tokenizer.symbol() == ")"
        while not finished:
            # Recognize var_type
            if t_type == Token_Types.keyword:
                var_type = self.tokenizer.keyWord()
            elif t_type == Token_Types.identifier:
                var_type = self.tokenizer.identifier()
            else:
                raise KeyError("Got some weird type in paramlist: " + t_type.value)
            self.tokenizer.advance()

            # Write var name
            var_name = self.tokenizer.identifier()
            self.tokenizer.advance()

            # Add the variable as an argument to the symbol table
            self.symbol_table.define(var_name, var_type, ARGS)

            t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
            if symbol == ')':
                finished = True
            else:
                self.eat(',')
                t_type = self.tokenizer.token_type()

    def compile_var_dec(self):
        """
        Compiles a var declaration
        :return:
        """
        # First word is valid.
        self.eat('var')

        # Second word is type.
        if self.tokenizer.token_type() == Token_Types.keyword:
            var_type = self.tokenizer.keyWord()
            if var_type not in ["int", "char", "boolean"]:
                raise Exception("Cant compile variable declaration with invalid keyword type.")
            self.write("<keyword> " + var_type + " </keyword>")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == Token_Types.identifier:
            var_type = self.tokenizer.identifier()
            self.tokenizer.advance()
        else:
            raise Exception("Cant compile variable declaration with invalid identifier type.")

        # Third and so on, are variables names.
        var_name = self.tokenizer.identifier()
        # Add the variable as an local to the symbol table
        self.symbol_table.define(var_name, var_type, LOCAL)
        self.tokenizer.advance()
        self.possible_varName(var_type, LOCAL)

        # It will always end with ';'
        self.eat(';')

# End of Subroutine Compilation logic ---------------------------------------------------

    def compile_statements(self):
        """
        Compile a sequence of 0 or more statements, not including the "{}".
        """
        # if self.tokenizer.token_type() != Token_Types.keyword:
        #     return
        #     # raise Exception("Can't use compile_statement if the current token isn't a keyword.")
        # statement = self.tokenizer.keyWord()
        # if statement not in ['let', 'if', 'while', 'do', 'return']:
        #     return
        # self.write("statements", True)
        # self.num_spaces += 1

        self.possible_single_statement()

        # self.num_spaces -= 1
        # self.write("statements", True, True)

    def possible_single_statement(self):
        """
        Compile 0 or more single statements..
        """
        if (self.tokenizer.token_type() == Token_Types.keyword and
                    self.tokenizer.keyWord() in STATEMENTS):

        # if self.tokenizer.keyWord() in STATEMENTS:
            statement = self.tokenizer.keyWord()
            # self.write(statement + "Statement", True)
            if statement == 'let':
                self.compile_let()
            elif statement == 'if':
                self.compile_if()
            elif statement == 'while':
                self.compile_while()
            elif statement == 'do':
                self.compile_do()
            elif statement == 'return':
                self.compile_return()
            # else:
            #     raise Exception("Invalid statement.")
            # self.write(statement + "Statement", True, True)
            self.possible_single_statement()

    def compile_do(self):
        """
        Compile do statement.
        :return:
        """
        self.eat('do')


        # self.num_spaces += 1
        # self.write("<keyword> do </keyword>")

        # is the check is necessary?  probably not..
        # if type != Token_Types.identifier:
        #     raise Exception()
        # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")

        # get variable / class name
        num_of_expressions = 0
        call_apparatus = self.tokenizer.identifier()
        # self.tokenizer.advance()  #todo: advance here or not?
        # If we encountered a variable or class name   (class.subroutine)
        if self.tokenizer.lookahead("."):
            kind = self.symbol_table.kind_of(call_apparatus)
            if kind: # this is a recognized variable name
                type = self.symbol_table.type_of(call_apparatus)  #todo: what do i do with type
                index = self.symbol_table.index_of(call_apparatus)
                self.writer.write_push(kind, index)
                num_of_expressions += 1    # this adds a self arg as one of the arguments.
            else:   # this is an unrecognized class name
                pass  #todo:what?
            self.eat(".")
        else:  # encounters a subroutine only
            self.writer.write_push(POINTER, 0)
            # Add to this function name the class name
            call_apparatus = self.class_name + "." + call_apparatus
            num_of_expressions += 1
        self.tokenizer.advance()
        self.eat('(')
        num_of_expressions += self.compile_expression_list()
        self.eat(')')
        # self.subroutineCall_continue()
        self.writer.write_pop("temp", 0)

        self.eat(';')
        self.writer.write_call(call_apparatus, num_of_expressions)
        # self.write("<symbol> ; </symbol>")
        # self.num_spaces -= 1


    def compile_let(self):
        """
        Compile let statement.
        """
        self.eat('let')
        # self.num_spaces += 1
        # self.write("<keyword> let </keyword>")
        symbol = self.tokenizer.identifier()
        segment = self.symbol_table.kind_of(symbol)
        index = self.symbol_table.index_of(symbol)
        # todo: need to write this symbol. if its a field need to add "push this 0"
        # self.compile_var_dec()
        # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        # self.write_terminal("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()
        self.possible_array()

        self.eat('=')
        # self.write("<symbol> = </symbol>")

        self.compile_expression()

        self.eat(';')

        self.writer.write_pop(segment, index)
        # self.write("<symbol> ; </symbol>")
        # self.num_spaces -= 1
        # self.write("</letStatement>")

    def possible_array(self):
        """
        Compile 0 or 1 array.
        """
        try:
            self.eat('[')
        except:
            # There is no array
            return
        # There is an array
        self.write("<symbol> [ </symbol>")
        self.compile_expression()
        self.eat(']')
        self.write("<symbol> ] </symbol>")

    def compile_while(self):
        """
        Compile while statement.
        """
        self.eat('while')
        label_loop, label_continue = self.__gen_while_label()
        self.writer.write_label(label_loop)
        self.eat('(')

        self.compile_expression()
        self.eat(')')
        self.writer.write_arithmetic("~")  #negate expression
        self.writer.write_if(label_continue)

        self.eat('{')
        self.compile_statements()
        self.eat('}')

        self.writer.write_goto(label_loop)
        self.writer.write_label(label_continue)


    def compile_return(self):
        """
        Compile return statement.
        """
        self.eat('return')
        # self.num_spaces += 1
        # self.write("<keyword> return </keyword>")

        if self.cur_func_type == "void":
            self.writer.write_push(CONSTANT, 0)
        else:
            try:
                self.eat(';')
            except:  # would it work?
                self.compile_expression()
                self.eat(';')

        self.writer.write_return()

        # self.write("<symbol> ; </symbol>")
        # self.num_spaces -= 1


    def compile_if(self):
        """
        Compile if statement.
        """
        true_label, false_label, cont_label = self.__gen_if_label()
        self.eat('if')

        self.eat('(')
        self.compile_expression()
        self.eat(')')
        self.writer.write_if(true_label)
        self.writer.write_goto(false_label)
        self.writer.write_label(true_label)

        self.eat('{')
        self.compile_statements()
        self.eat('}')
        if self.tokenizer.lookahead("else"):
            self.eat("else")
            self.eat('{')
            self.writer.write_goto(cont_label)
            self.writer.write_label(false_label)
            self.compile_statements()
            self.eat('}')
            self.writer.write_label(cont_label)
        else:
            self.writer.write_label(false_label)

    # def possible_else(self):
    #     """
    #     Compile 0 or 1 else sections.
    #     """
    #     try:
    #         self.eat('else')
    #     except:
    #         # There is no else so we can return
    #         return
    #
    #     # There is an else, so we handle it properly
    #
    #
    #     self.eat('{')
    #
    #     self.compile_statements()
    #     self.eat('}')


    def compile_expression(self, from_op_term=False):
        """
        Compile an expression.
        :return:
        """

        if self.tokenizer.token_type() == Token_Types.symbol:
            if self.tokenizer.symbol() == '(':
                # There is an open bracket
                self.tokenizer.advance()
                self.compile_expression()

                if self.tokenizer.token_type() == Token_Types.symbol:
                    if self.tokenizer.symbol() == ')':
                        self.tokenizer.advance()
                else:
                    raise Exception("There more '(' than ')', while compiling expression.")

                if not from_op_term:
                    self.possible_op_term()
                return

        # There is no open bracket
        self.compile_term()
        self.possible_op_term()

    def subroutineCall_continue(self, func, is_method):
        """
        After an identifier there can be a '.' or '(', otherwise it not function call
        (subroutineCall).
        :return:
        """
        # should i check every time if it's type symbol?
        symbol = self.tokenizer.symbol()
        if symbol == '(':
            self.eat('(')
            num_exp = self.compile_expression_list()
            self.eat(')')
            self.writer.write_call(func, num_exp)

        elif symbol == '.':
            self.eat('.')
            if is_method:
                object = func # The object name
                segment, index = self.symbol_table.kind_of(object), self.symbol_table.index_of(object)
                # what is happening if the kind is field?
                if segment == "field":
                    self.writer.write_push(POINTER, 0)
                    segment = THIS
                self.writer.write_push(segment, index)
                func = self.tokenizer.identifier()
            else:
                func += "." + self.tokenizer.identifier()
            self.tokenizer.advance()

            self.eat('(')
            num_exp = self.compile_expression_list()
            self.eat(')')
            self.writer.write_call(func, num_exp)

        else:
            raise Exception("If there is a symbol in the subroutineCall it have to be . or (.")

    def compile_term(self):
        """
        Compiles a temp. This routine is faced with a slight difficulty when trying to
        decide between some of the alternative parsing rules. Specifically,
        if the current token is an identifier, the routine must distinguish between a
        variable, an array entry, and a subroutine call. A single look-ahead token,
        which may be one of "[", "(", or "." suffices to distiguish between the three
        possibilities. Any other token is not part of this term and should not be
        advanced over.
        :return:
        """
        type = self.tokenizer.token_type()

        # If the token is a int_const
        if type == Token_Types.int_const :
            self.writer.write_push(CONSTANT, self.tokenizer.intVal())
            self.tokenizer.advance()

        # If the token is a string_const
        elif type == Token_Types.string_const:
            str_const = self.tokenizer.stringVal()
            self.writer.write_push(CONSTANT, len(str_const) - 1)
            self.writer.write_call(BuiltinFunctions.str_new, 1)
            for i in range(len(str_const)):
                self.writer.write_push(CONSTANT, ord(str_const[i]))
                self.writer.write_call(BuiltinFunctions.str_new.str_app_char, 1)

        # If the token is a keyword
        elif type == Token_Types.keyword:
            word = self.tokenizer.keyWord()
            if word in ["false", "null"]:
                self.writer.write_push(CONSTANT, 0)
            elif word == "true":
                self.writer.write_push(CONSTANT, -1)
            elif word == "this":
                self.writer.write_push(POINTER, 0)
            else:
                raise Exception()
            self.tokenizer.advance()

        # If the token is an identifier
        elif type == Token_Types.identifier:
            name = self.tokenizer.identifier()
            kind, index = self.symbol_table.kind_of(name), self.symbol_table.index_of(name)
            if kind == "field":
                # Using 'this'
                self.writer.write_push(POINTER, 0)
                self.writer.write_push(THIS, index)
            elif not kind:
                self.writer.write_push(kind, index)

            is_object = True if index else False
            self.tokenizer.advance()
            self.possible_identifier_continue(name, is_object)

        # If the token is an symbol
        elif type == Token_Types.symbol:
            if self.tokenizer.symbol() == '(':
                self.compile_expression()
            elif self.tokenizer.symbol() in ["-", "~"]:
                # self.write("<symbol> " + self.tokenizer.symbol() + " </symbol>", use_buffer=True)
                self.eat(self.tokenizer.symbol())
                # self.write("<symbol> " + self.tokenizer.symbol() + " </symbol>")
                self.compile_term()
                command = "neg" if self.tokenizer.symbol() == "-" else "not"
                self.writer.write_arithmetic(command)
            else:
                # self.cleanbuffer()
                raise Exception()

        else:
            raise Exception("Invalid token for creating term.")

    def possible_identifier_continue(self, identifier_val, is_obj):
        """
        In a term if identifier continues with
        - '[' - it's a call of an array
        - '.' or '('  - it's part of subroutineCall (function call)
        - nothing - it's a variable
        This functions handle every one of this situations after the original identifier was
        handled.
        """
        if self.tokenizer.token_type() == Token_Types.symbol:
            # todo: make sure working with arrays works well.
            # how to i handle A[a] = B[b]
            if self.tokenizer.symbol() == '[':
                self.eat('[')
                self.compile_expression() # do i nead to make sure it's not const string?
                self.eat(']')
                self.writer.write_arithmetic('add')
                self.writer.write_pop("pointer", 1)
                self.writer.write_push("that", 0)
                return

            try:
                self.subroutineCall_continue(identifier_val, is_obj)
            except Exception:
                # raise Exception("If there is a symbol in the token it have to be . or [ or (.")
                return

    def possible_op_term(self):
        """
        If the next token is a suitable operation symbol than compile more terms,
        otherwise return nothing.
        """
        # There is no op term
        if self.tokenizer.token_type() != Token_Types.symbol:
            return
        op = self.tokenizer.symbol()
        if op not in OPERANDS:
            return

        # There is op term
        self.tokenizer.advance()
        if self.tokenizer.token_type() == Token_Types.symbol:
            if op == '(':
                self.compile_expression(True)
        else:
            self.compile_term()

        self.handle_op(op)
        self.possible_op_term()

    def handle_op(self, op):
        if op == '+':
            self.writer.write_arithmetic('add')
        elif op == '-':
            self.writer.write_arithmetic('sub')
        elif op == '*':
            self.writer.write_call(BuiltinFunctions.math_mult, 0)
        elif op == '/':
            self.writer.write_call(BuiltinFunctions.math_div, 0)
        elif op == '=':
            self.writer.write_arithmetic('eq')
        elif op == '&gt':
            self.writer.write_arithmetic('gt')
        elif op == '&lt':
            self.writer.write_arithmetic('lt')
        elif op == '&amp':
            self.writer.write_arithmetic('and')
        elif op == '|':
            self.writer.write_arithmetic('or')
        else:
            raise Exception(op + " is an invalid operation between 2 terms.") # wont happen according to the current use

    def compile_expression_list(self):
        """
        Compile a comma-separated list of expressions, which may be empty.
        """
        try:
            self.compile_expression()
        except Exception:
            return 0

        return self.possible_more_expression() + 1

    # def possible_more_expression(self, exp_count):
    #     return self.possible_more_expression() + 1
    #     # self.num_spaces -= 1
    #     # self.write("expressionList", True, True)


    def possible_more_expression(self):
        """
        If the next token is a ',' than compile more expressions,
        otherwise return nothing.
        """
        try:
            self.eat(',')
        except Exception:
            return 0

        self.compile_expression()
        return self.possible_more_expression() + 1


#-------------------------------------------------------------------------------------
    def write(self, statement, delim = False, end = False, new_line=True,
              no_space = False, use_buffer=False):
        """

        :param statement:
        :return:
        """
        if use_buffer:
            self.output.write(self.buffer)
            self.buffer = ""
        if end:
            statement = "/" + statement
        if delim:
            statement = "<" + statement + ">"
        if not no_space:
            statement = SPACE * self.num_spaces + statement
        if new_line:
            statement += END_LINE


        self.output.write(statement)

        # if delim:
        #     self.output.write(TAB * self.num_spaces + "<" + statement + ">")
        # else:

        # if new_line:
        #     self.output.write(END_LINE)

    def write_terminal(self, t_type, arg):
        """

        :param t_type:
        :param arg:
        :return:
        """
        self.write(t_type, delim=True, new_line=False, no_space=False)
        self.write(" " + arg + " ", delim=False, new_line=False, no_space=True)
        self.write(t_type, delim=True, new_line=True, end=True, no_space=True)

    def cleanbuffer(self):
        self.num_spaces -= 1
        self.buffer = ""



    # def write_recursive(self, name, advance_lim=1):
    #     """
    #
    #     :param name:
    #     :param advance_lim:
    #     :return:
    #     """
    #     self.write(name, num_tabs=self.indent)
    #
    #     self.indent += 1
    #     self.call_single()
    #     for _ in range(advance_lim - 1):
    #         if self.tokenizer.has_more_tokens():
    #             self.tokenizer.advance()
    #             self.call_single()
    #         else:
    #             raise ValueError("expected more tokens")
    #
    #     # self.write(name + " " + arg, delim=False,
    #     #            num_tabs=self.indent + 1)
    #     self.write(name, num_tabs=self.indent, end=True)


    # def write_recursive(self, type):
    #     """
    #
    #     :param type:
    #     :return:
    #     """
    #     self.write(type.value, num_tabs=self.indent)
    #     self.indent += 1
    #
    #     # need some sort of termination in call compile
    #     # or type specific implementation
    #     self.full_recursion()
    #
    #     self.write(type.value, num_tabs=self.indent, end=True)



    # def full_recursion(self):
    #     """
    #
    #     :param token:
    #     :return:
    #     """
    #     while self.tokenizer.has_more_tokens():
    #         self.tokenizer.advance()
    #
    #         type = self.tokenizer.token_type()
    #
    #         terminal_arg = False
    #
    #         if type == Token_Types.keyword:
    #             terminal_arg = self.tokenizer.keyWord()
    #
    #         if type == Token_Types.symbol:
    #             terminal_arg = self.tokenizer.symbol()
    #
    #         if type == Token_Types.identifier:
    #             terminal_arg = self.tokenizer.identifier()
    #
    #         if type == Token_Types.int_const:
    #             terminal_arg = self.tokenizer.intVal()
    #
    #         if type == Token_Types.string_const:
    #             terminal_arg = self.tokenizer.stringVal()
    #
    #         if terminal_arg:
    #             self.write_terminal(type, terminal_arg)
    #
    #         else:
    #             self.write_recursive(type)


    # def call_single(self):
    #     """
    #
    #     :return:
    #     """
    #     type = self.tokenizer.token_type()
    #
    #     terminal_arg = False
    #
    #     if type == Token_Types.keyword:
    #         terminal_arg = self.tokenizer.keyWord()
    #
    #     if type == Token_Types.symbol:
    #         terminal_arg = self.tokenizer.symbol()
    #
    #     if type == Token_Types.identifier:
    #         terminal_arg = self.tokenizer.identifier()
    #
    #     if type == Token_Types.int_const:
    #         terminal_arg = self.tokenizer.intVal()
    #
    #     if type == Token_Types.string_const:
    #         terminal_arg = self.tokenizer.stringVal()
    #
    #     if terminal_arg:
    #         self.write_terminal(type, terminal_arg)
    #
    #     else:
    #         self.write_recursive(type)

    def __gen_while_label(self):
        self.__label_counter[WHILE] += 1
        return ("WHILE_LOOP" + str(self.__label_counter[WHILE]), "WHILE_CONT" + str(
            self.__label_counter[WHILE]))


    def __gen_if_label(self):
        self.__label_counter[IF] += 1
        return ("IF_TRUE" + str(self.__label_counter[IF]), "IF_FALSE" + str(
            self.__label_counter[IF]), "IF_CONT" + str(self.__label_counter[IF]))

    def __reset_label_counter(self):
        self.__label_counter = [0, 0]



