import unittest
from lexer import tokenize
from parser import Parser
from interpreter import Interpreter

class InterpreterTests(unittest.TestCase):
    def run_code(self, code):
        tokens = tokenize(code)
        parser = Parser(tokens)
        ast = parser.parse()
        interpreter = Interpreter()
        
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        interpreter.interpret(ast)
        
        sys.stdout = sys.__stdout__
        return captured_output.getvalue().strip()

    def test_var_and_print(self):
        code = """
        var a = 3
        print a
        """
        output = self.run_code(code)
        self.assertEqual(output, "3")

    def test_arithmetic(self):
        code = """
        var a = 3 + 4 * 2
        print a
        """
        output = self.run_code(code)
        self.assertEqual(output, "11")

    def test_if_else(self):
        code = """
        var a = 5
        if a > 3 {
            print "yes"
        } else {
            print "no"
        }
        """
        output = self.run_code(code)
        self.assertEqual(output, "yes")

    def test_while_loop(self):
        code = """
        var i = 0
        while i < 3 {
            print i
            var i = i + 1
        }
        """
        output = self.run_code(code)
        self.assertEqual(output, "0\n1\n2")

    def test_for_loop(self):
        code = """
        for var i = 0 i < 10 i = i + 1 {
            print i
        }
        """
        output = self.run_code(code)
        self.assertEqual(output, "0\n1\n2\n3\n4\n5\n6\n7\n8\n9")
        #check

if __name__ == "__main__":
    unittest.main()