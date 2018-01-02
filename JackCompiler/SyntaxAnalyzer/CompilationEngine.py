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
        self.tokenizer = JackTokenizer(input_file)
        self.num_spaces = 0
        self.buffer = ""
        with open(output_file, 'w') as self.output:
            while self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                assert self.tokenizer.token_type() == Token_Types.keyword
                if self.tokenizer.keyWord() == 'class':
                    self.compile_class()
                else:
                    raise KeyError("Received a token that does not fit the beginning of a "
                                   "module. " + self.tokenizer.keyWord()
                                   + " in " + input_file)

    def compile_class(self):
        """
        Compiles a complete class
        :return:
        """
        self.write('class', delim=True)
        self.num_spaces += 1
        self.write_terminal(self.tokenizer.token_type().value, self.tokenizer.keyWord())
        self.eat('class')

        t_type, class_name = self.tokenizer.token_type(), self.tokenizer.identifier()
        self.write_terminal(t_type.value, class_name)

        self.tokenizer.advance()

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
        self.write_terminal(t_type.value, symbol)
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

        self.write_terminal(t_type.value, self.tokenizer.symbol())
        self.num_spaces -= 1
        self.write('class', delim=True, end=True)

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
        self.write("classVarDec", True)
        self.num_spaces += 1

        # First word is static or field.

        # if self.tokenizer.token_type() != Token_Types.keyword:
        #     raise Exception("Cant compile class variable declaration without keyword token.")

        # should i check before if i can get a keyword?
        var_sort = self.tokenizer.keyWord()
        if var_sort not in ["static", "field"]:
            raise Exception("Cant compile class variable declaration without static of field.")
        self.write("<keyword> " + var_sort + " </keyword>")
        self.tokenizer.advance()

        # Second word is type.
        if self.tokenizer.token_type() == Token_Types.keyword:
            var_type = self.tokenizer.keyWord()
            if var_type not in ["int", "char", "boolean"]:
                raise Exception("Cant compile class variable declaration with invalid keyword type.")
            self.write("<keyword> " + var_type + " </keyword>")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == Token_Types.identifier:
            self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
            self.tokenizer.advance()
        else:
            raise Exception("Cant compile class variable declaration with invalid identifier type.")

        # Third and so on, are variables names.
        # if self.tokenizer.token_type() != Token_Types.identifier:
        #     raise Exception("Cant compile class variable declaration without varName identifier.")
        # assert self.tokenizer.token_type() == Token_Types.identifier
        self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.tokenizer.advance()
        self.possible_varName()

        # It will always end with ';'
        self.eat(';')
        self.write("<symbol> ; </symbol>")

        self.num_spaces -= 1
        self.write("classVarDec", True, True)

    def possible_varName(self):
        """
        Compile 0 or more variable names, after an existing variable name.
        """
        try:
            self.eat(',')
        except:
            # There is no varName
            return
        # There is an varName
        self.write("<symbol> , </symbol>")
        # if self.tokenizer.token_type() != Token_Types.identifier:
        #     raise Exception("Cant compile (class or not) variable declaration without varName" +
        #                     " identifier after ',' .")
        self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.tokenizer.advance()
        self.possible_varName()

    def compile_subroutine(self):
        """
        Compiles a complete method, function or constructor
        :return:
        """
        self.write('subroutineDec', delim=True)
        self.num_spaces += 1
        self.write_terminal(self.tokenizer.token_type().value, self.tokenizer.keyWord())

        # self.eat('function' | 'method' | 'constructor')
        self.tokenizer.advance()

        t_type = self.tokenizer.token_type()
        if t_type == Token_Types.keyword:
            func_type = self.tokenizer.keyWord()
        else:
            func_type = self.tokenizer.identifier()
        self.write_terminal(t_type.value, func_type)

        # self.eat('void' | some other type)
        self.tokenizer.advance()

        t_type, func_name = self.tokenizer.token_type(), self.tokenizer.identifier()
        self.write_terminal(t_type.value, func_name)

        self.tokenizer.advance()

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
        self.write_terminal(t_type.value, symbol)
        self.eat('(')

        self.compile_param_list()

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
        self.write_terminal(t_type.value, symbol)
        self.eat(')')

        self.write("subroutineBody", delim=True)

        self.num_spaces += 1

        t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
        self.write_terminal(t_type.value, symbol)
        self.eat('{')



        t_type = self.tokenizer.token_type()
        while t_type != Token_Types.symbol:
            token = self.tokenizer.keyWord()
            if token == 'var':
                self.compile_var_dec()
            elif token in STATEMENTS:
                self.compile_statements()
            else:
                raise KeyError("an unknown step inside a subroutine")
            # self.tokenizer.advance()
            t_type = self.tokenizer.token_type()

        self.write_terminal(t_type.value, self.tokenizer.symbol())
        self.eat('}')

        self.num_spaces -= 1

        self.write("subroutineBody", delim=True, end=True)

        self.num_spaces -= 1
        self.write('subroutineDec', delim=True, end=True)


    def compile_param_list(self):
        """
        Compiles a parameter list, which may be empty, not including the "()"
        :return:
        """
        self.write('parameterList', delim=True)
        self.num_spaces += 1

        t_type = self.tokenizer.token_type()
        finished = t_type == Token_Types.symbol and self.tokenizer.symbol() == ")"
        while not finished:
            # Recognized type
            if t_type == Token_Types.keyword:
                token = self.tokenizer.keyWord()
            elif t_type == Token_Types.identifier:
                token = self.tokenizer.identifier()
            else:
                raise KeyError("Got some weird type in paramlist: " + t_type.value)

            # Write var type
            self.write_terminal(t_type.value, token)

            self.tokenizer.advance()

            # Write var name
            t_type, token = self.tokenizer.token_type(), self.tokenizer.identifier()
            self.write_terminal(t_type.value, token)

            self.tokenizer.advance()

            t_type, symbol = self.tokenizer.token_type(), self.tokenizer.symbol()
            if symbol == ')':
                finished = True
            else:
                self.eat(',')
                self.write_terminal(t_type.value, symbol)
                t_type = self.tokenizer.token_type()



        self.num_spaces -= 1
        self.write('parameterList', delim=True, end=True)

    def compile_var_dec(self):
        """
        Compiles a var declaration
        :return:
        """
        self.write("varDec", True)
        self.num_spaces += 1

        # First word is valid.
        self.eat('var')
        self.write("<keyword> var </keyword>")

        # Second word is type.
        if self.tokenizer.token_type() == Token_Types.keyword:
            var_type = self.tokenizer.keyWord()
            if var_type not in ["int", "char", "boolean"]:
                raise Exception("Cant compile variable declaration with invalid keyword type.")
            self.write("<keyword> " + var_type + " </keyword>")
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == Token_Types.identifier:
            self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
            self.tokenizer.advance()
        else:
            raise Exception("Cant compile variable declaration with invalid identifier type.")

        # Third and so on, are variables names.
        # if self.tokenizer.token_type() != Token_Types.identifier:
        #     raise Exception("Cant compile variable declaration without varName identifier.")
        self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.tokenizer.advance()
        self.possible_varName()

        # It will always end with ';'
        self.eat(';')
        self.write("<symbol> ; </symbol>")

        self.num_spaces -= 1
        self.write("varDec", True, True)

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
        self.write("statements", True)
        self.num_spaces += 1

        self.possible_single_statement()

        self.num_spaces -= 1
        self.write("statements", True, True)

    def possible_single_statement(self):
        """
        Compile 0 or more single statements..
        """
        if (self.tokenizer.token_type() == Token_Types.keyword and
                    self.tokenizer.keyWord() in STATEMENTS):

        # if self.tokenizer.keyWord() in STATEMENTS:
            statement = self.tokenizer.keyWord()
            self.write(statement + "Statement", True)
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
            self.write(statement + "Statement", True, True)
            self.possible_single_statement()

    def compile_do(self):
        """
        Compile do statement.
        :return:
        """
        self.eat('do')
        self.num_spaces += 1
        self.write("<keyword> do </keyword>")

        # is the check is necessary?  probably not..
        # if type != Token_Types.identifier:
        #     raise Exception()
        self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.tokenizer.advance()
        self.subroutineCall_continue()

        self.eat(';')
        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1


    def compile_let(self):
        """
        Compile let statement.
        """
        self.eat('let')
        self.num_spaces += 1
        self.write("<keyword> let </keyword>")

        # self.compile_var_dec()
        # self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
        self.write_terminal("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()
        self.possible_array()

        self.eat('=')
        self.write("<symbol> = </symbol>")

        self.compile_expression()

        self.eat(';')
        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1
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
        # self.write("<whileStatement>")
        self.num_spaces += 1
        self.write("<keyword> while </keyword>")

        self.eat('(')
        self.write("<symbol> ( </symbol>")
        self.compile_expression()
        self.eat(')')
        self.write("<symbol> ) </symbol>")

        self.eat('{')
        self.write("<symbol> { </symbol>")
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>")

        self.num_spaces -= 1
        # self.write("</whileStatement>")

    def compile_return(self):
        """
        Compile return statement.
        """
        self.eat('return')
        self.num_spaces += 1
        self.write("<keyword> return </keyword>")

        try:
            self.eat(';')
        except: # would it work?
            self.compile_expression()
            self.eat(';')

        self.write("<symbol> ; </symbol>")
        self.num_spaces -= 1


    def compile_if(self):
        """
        Compile if statement.
        """
        self.eat('if')
        # self.write("<ifStatement>")
        self.num_spaces += 1
        self.write("<keyword> if </keyword>")

        self.eat('(')
        self.write("<symbol> ( </symbol>")
        self.compile_expression()
        self.eat(')')
        self.write("<symbol> ) </symbol>")

        self.eat('{')
        self.write("<symbol> { </symbol>")
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>")
        self.possible_else()

        self.num_spaces -= 1
        # self.write("</ifStatement>" + END_LINE)

    def possible_else(self):
        """
        Compile 0 or 1 else sections.
        """
        try:
            self.eat('else')
        except:
            # There is no else so we can return
            return

        # There is an else, so we handle it properly
        self.write("<keyword> else </keyword>")

        self.eat('{')
        self.write("<symbol> { </symbol>")
        self.compile_statements()
        self.eat('}')
        self.write("<symbol> } </symbol>")

    def compile_expression(self):
        """
        Compile an expression.
        :return:
        """
        self.buffer += self.num_spaces * SPACE + "<expression>\n"
        self.num_spaces += 1
        try:
            self.compile_term()
            self.possible_op_term()
            self.num_spaces -= 1
            self.write("expression", True, True)
        except:
            self.cleanbuffer()



    def subroutineCall_continue(self):
        """
        After an identifier there can be a '.' or '(', otherwise it not function call
        (subroutineCall).
        :return:
        """
        # should i check every time if it's type symbol?
        symbol = self.tokenizer.symbol()
        if symbol == '(':
            self.eat('(')
            self.write("<symbol> ( </symbol>")
            self.compile_expression_list()
            self.eat(')')
            self.write("<symbol> ) </symbol>")

        elif symbol == '.':
            self.eat('.')
            self.write("<symbol> . </symbol>")

            self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>")
            self.tokenizer.advance()

            self.eat('(')
            self.write("<symbol> ( </symbol>")
            self.compile_expression_list()
            self.eat(')')
            self.write("<symbol> ) </symbol>")

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
        self.buffer += SPACE * self.num_spaces + "<term>\n"
        self.num_spaces += 1

        type = self.tokenizer.token_type()
        # maybe i should divide it for int and string
        # If the token is a string_const or int_const
        if type in [Token_Types.string_const, Token_Types.int_const] :
            value = self.tokenizer.intVal() if type == Token_Types.int_const else self.tokenizer.stringVal()
            self.write("<" + type.value + "> " +
                       value +
                       " </" + type.value + ">", use_buffer=True)
            self.tokenizer.advance()

        # If the token is a keyword
        elif type == Token_Types.keyword:
            if self.tokenizer.keyWord() in KEY_TERMS:
                self.write("<" + type.value + "> " +
                           self.tokenizer.keyWord() +
                           " </" + type.value + ">", use_buffer=True)
                self.tokenizer.advance()
            else:
                self.cleanbuffer()
                raise Exception()

        # If the token is an identifier
        elif type == Token_Types.identifier:
            # value = self.tokenizer.identifier()
            self.write("<identifier> " + self.tokenizer.identifier() + " </identifier>",
                       use_buffer=True)
            self.tokenizer.advance()
            self.possible_identifier_continue()

        # If the token is an symbol
        elif type == Token_Types.symbol:

            if self.tokenizer.symbol() == '(':
                self.eat('(')
                self.write("<symbol> ( </symbol>", use_buffer=True)
                self.compile_expression()
                self.eat(')')
                self.write("<symbol> ) </symbol>")
            elif self.tokenizer.symbol() in ["-", "~"]:
                self.write("<symbol> " + self.tokenizer.symbol() + " </symbol>", use_buffer=True)
                self.eat(self.tokenizer.symbol())
                # self.write("<symbol> " + self.tokenizer.symbol() + " </symbol>")
                self.compile_term()
            else:
                self.cleanbuffer()
                raise Exception()

        else:
            raise Exception("Invalid token for creating term.")

        self.num_spaces -= 1
        self.write("term", True, True)

    def possible_identifier_continue(self):
        """
        In a term if identifier continues with
        - '[' - it's a call of an array
        - '.' or '('  - it's part of subroutineCall (function call)
        - nothing - it's a variable
        This functions handle every one of this situations after the original identifier was
        handled.
        """
        # try:
        #     self.eat("[")
        # except:
        # if not self.tokenizer.has_more_tokens(): # already doing it by itself
        #     raise Exception()
        if self.tokenizer.token_type() == Token_Types.symbol:
            if self.tokenizer.symbol() == '[':
                self.eat('[')
                self.write("<symbol> [ </symbol>")
                self.compile_expression()
                self.eat(']')
                self.write("<symbol> ] </symbol>")
                return

            try:
                self.subroutineCall_continue()
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
            # raise Exception("After term can be only nothing or (op term)*.")
            return
        op = self.tokenizer.symbol()

        if op not in OPERANDS:
            # raise Exception("Invalid operator use in term.")
            return # should it be like this?

        try:
            # if op in SPECIAL_SYMBOL.keys():
            #     op = SPECIAL_SYMBOL[op]
            self.eat(op)
        except Exception:
            return
        # There is op term
        self.write("<symbol> " + op + " </symbol>")
        self.compile_term()

        self.possible_op_term()

    def compile_expression_list(self):
        """
        Compile a comma-separated list of expressions, which may be empty.
        """
        self.write("expressionList", True)
        self.num_spaces += 1

        try:
            self.compile_expression()
        except Exception:
            self.num_spaces -= 1
            self.write("expressionList", True, True)
            return



        self.possible_more_expression()
        self.num_spaces -= 1
        self.write("expressionList", True, True)

    def possible_more_expression(self):
        """
        If the next token is a ',' than compile more expressions,
        otherwise return nothing.
        """
        try:
            self.eat(',')
        except Exception:
            return
        self.write("<symbol> , </symbol>")
        self.compile_expression()

        self.possible_more_expression()

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





