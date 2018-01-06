"""

"""

from JackCompiler.SyntaxAnalyzer.CompilationEngine import CompilationEngine

from JackCompiler.SyntaxAnalyzer.JackTokenizer import JackTokenizer

FILE_PATH = 1

FILE_EXTENSION_XML = '.xml'
FILE_EXTENSION_JACK = '.jack'
FILE_EXTENSION_VM = '.vm'

class Analyzer():
    """

    :param filename:
    :return:
    """
    def __init__(self):
        pass

    def tokenize(self, source, destination):
        tokenizer = JackTokenizer(source)
        with open(destination, 'w') as out:
            out.write("<tokens>\n")
            while tokenizer.has_more_tokens():
                tokenizer.advance()
                out.write("<" + tokenizer.token_type().value + "> "
                          + tokenizer.cur_val + " </" +
                          tokenizer.token_type().value + ">\n")
            out.write("</tokens>\n")

    def compile(self, source, destination):
        engine = CompilationEngine(source, destination)


if __name__ == '__main__':

    a = Analyzer()
    a.tokenize("tests/ExpressionLessSquare")

