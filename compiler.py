import re
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter


def main():
    code = """
    var a = 3 + 4
    print a
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter()
    interpreter.interpret(ast)




if __name__ == "__main__":
    main()