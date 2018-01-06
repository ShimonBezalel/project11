"""

"""
from enum import Enum, unique

import re


@unique
class Token_Types(Enum):
    """

    """
    keyword         = "keyword"
    symbol          = "symbol"
    identifier      = "identifier"
    int_const       = "integerConstant"
    string_const    = "stringConstant"


@unique
class Key_Words(Enum):
    """

    """
    class_key       = "CLASS"
    method          = "METHOD"
    function        = "FUNCTION"
    constructor     = "CONSTRUCTOR"
    int_key         = "INT"
    bool_key        = "BOOLEAN"
    char_key        = "CHAR"
    void_key        = "VOID"
    var_key         = "VAR"
    static_key      = "STATIC"
    field_key       = "FIELD"
    let_key         = "LET"
    do_key          = "DO"
    if_key          = "IF"
    else_key        = "ELSE"
    while_key       = "WHILE"
    return_key      = "RETURN"
    true_key        = "TRUE"
    false_key       = "FALSE"
    null_key        = "NULL"
    this_key        = "THIS"


KEYWORDS = [key.value.lower() for key in Key_Words]

def gen_keywords():
    conc_str = ''
    for key in KEYWORDS:

        conc_str += key + "\\s|"

    return conc_str[:-1]

def gen_symbols():
    conc_str = ''
    for symbol in symbols:
        conc_str += "\\" + symbol + "|"
    return conc_str[:-1]

symbols = {
    '{',
    '}',
    '(',
    ')',
    '[',
    ']',
    '.',
    ',',
    ';',
    '+',
    '-',
    '*',
    '/',
    '&',
    '|',
    '<',
    '>',
    '=',
    '~'
}




INT_CONST_MIN = 0
INT_CONST_MAX = 32767

class Comp_Exp(Enum):
    """

    """
    single_line_comment = re.compile("(\/\/.*)")
    doc_string = re.compile("(\/\*\*((([^*])*([^/])*)|(([^/])*([^*])*))\*\/)")
    # comment = re.compile("((\/\/.*)|(\/\*\*((([^*])*([^/])*)|(([^/])*([^*])*))\*\/))")
    string_single_line = re.compile("(\"((\\\\\")|([^\"]))*\")")
    keywords = re.compile(gen_keywords())
    symbols = re.compile(gen_symbols())
    floats = re.compile("((\d+\.\d+)|(\d+))")
    ints = re.compile("\d+")
    identifiers = re.compile("\w+")
    spaces = re.compile("(\s+\n?)+")


class JackTokenizer():
    """

    """
    def __init__(self, inputFile):
        """
        Opens the input file/stream and gets ready to tokenize it
        :param inputFile:
        """
        with open(inputFile, 'r') as self.file:
            self.text = self.file.read()

        # remove comments and save the result for parsing
        # self.text = Comp_Exp.comment.value.sub(" ", temp)

        # Generator object that retrieves tokens one at a time
        self.token_gen = self.token_gen()

        # A helping bool value for calibrating has-more and advance
        self.wait = False

        self.cur_type, self.cur_val = None, None

        self.tokens = list(self.token_gen)

        self.cur_pos = -1

    def has_more_tokens(self):
        """
        Any more tokens in input?
        :return: bool
        """
        return self.cur_pos < len(self.tokens) - 1

        try:
            self.cur_type, self.cur_val = self.token_gen.__next__()
            self.wait = True
            return True
        except StopIteration:
            return False

    def advance(self):
        """
        Get the next token and make it cur token. This method should only be called if
        has more tokens is true. There is no initial token in cur.
        :return:
        """
        self.cur_pos += 1
        self.cur_type, self.cur_val = self.tokens[self.cur_pos]
        return

        if self.wait:
            self.wait = False
        else:
            self.cur_type, self.cur_val = self.token_gen.__next__()

    def token_type(self):
        """
        Returns the type of the tokenizer
        :return:
        """
        return self.cur_type

    def keyWord(self):
        """
        Returns the keyword which is the current toekn. Should be called only when
        token_type is KEYWORD
        :return:
        """
        assert self.cur_type is Token_Types.keyword
        return self.cur_val

    def symbol(self):
        """
        Returns  a char representing current token. Only called when token_type is SYMBOL
        :return:  char
        """
        assert self.cur_type is Token_Types.symbol
        return self.cur_val

    def identifier(self):
        """
        Returns an identifier string representing current token. Only called when
        token_type is IDENTIFIER
        :return: String
        """
        assert self.cur_type is Token_Types.identifier
        return self.cur_val

    def intVal(self):
        """
        Returns an int value representing current token. Only called when token_type is
        INT_CONST
        :return: int
        """
        assert self.cur_type is Token_Types.int_const
        return self.cur_val

    def stringVal(self):
        """
        Returns a string representing current token. Only called when token_type is
        StringConst
        :return: string
        """
        assert self.cur_type is Token_Types.string_const
        return self.cur_val

    def token_gen(self):
        """

        :return:
        """
        # while True:
        while self.text:
            # In case of a token match, we yield it and substitute it from what is left
            # of the current line being read
            comment_match = Comp_Exp.single_line_comment.value.match(self.text)
            # todo: needs good comment implementation and testing
            if comment_match:
                self.text = self.text[comment_match.end():]
                continue

            docstring_match = Comp_Exp.doc_string.value.match(self.text)
            if docstring_match:
                self.text = self.text[docstring_match.end():]
                continue

            string_match = Comp_Exp.string_single_line.value.match(self.text)

            # Found a full string in what is left of the current line.
            # Note the string-const values have their "" symbols left out.
            if string_match:
                yield (Token_Types.string_const, string_match.group(0)[1:-1])
                self.text = self.text[string_match.end():]
                continue

            keyword_match = Comp_Exp.keywords.value.match(self.text) #self.cur_line)
            if keyword_match:
                # remove space
                yield (Token_Types.keyword, keyword_match.group(0)[:-1])
                self.text = self.text[keyword_match.end():]
                continue

            symbols_match = Comp_Exp.symbols.value.match(self.text)
            if symbols_match:
                symbol = symbols_match.group(0)
                if symbol == '<':
                    symbol = '&lt;'
                elif symbol == '>':
                    symbol = '&gt;'
                elif symbol == '\"': # its a '"' symbol. the \ is an escape char
                    symbol = '&quot;'
                elif symbol == '&':
                    symbol = '&amp;'
                yield (Token_Types.symbol, symbol)
                self.text = self.text[symbols_match.end():]
                continue

            int_match = Comp_Exp.ints.value.match(self.text)
            if int_match:
                yield (Token_Types.int_const, int_match.group(0))
                self.text = self.text[int_match.end():]
                continue

            identifier_match = Comp_Exp.identifiers.value.match(self.text)
            if identifier_match:
                word = identifier_match.group(0)

                # Here they may be a special case where a keyword was found without a
                # space after it, such as "return;". In this case this identifier
                # should rather be categorized at keyword, even though it previously
                # did not match
                if word in KEYWORDS:
                    yield (Token_Types.keyword, identifier_match.group(0))
                else:
                    yield (Token_Types.identifier, identifier_match.group(0))
                self.text = self.text[identifier_match.end():]
                continue

            space_match = Comp_Exp.spaces.value.match(self.text)
            if space_match:
                self.text = self.text[space_match.end():]
                continue

            else:
                raise StopIteration("found impossible situation: " + self.text)

    def lookahead(self, token, steps = 1):
        """
        Looks to see if the given token is the next token in the list of tokens,
        up to "steps" number of steps forward. If the list limitation is exceeded by
        the provided number of steps, then the steps are truncated.
        :param token: any string
        :param steps: number of steps to look forward. default is 1
        :return: True or False, if the symbol is within the number of steps,
        as an individual token
        """
        trunc = min(len(self.tokens), self.cur_pos + steps + 1)
        for i in range(self.cur_pos + 1, trunc):
            if token == self.tokens[i][1]:
                return True
        return False


if __name__ == '__main__':

    pass















