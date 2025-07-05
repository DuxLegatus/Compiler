import re
tokens_types = ["VAR","PRINT","IDENTIFIER","NUMBER","OPERATOR","EQUAL","LPAREN","RPAREN","COMMENT"]
token_regex = (
    r'(?P<VAR>var)|'
    r'(?P<PRINT>print)|'
    r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)|'
    r'(?P<NUMBER>[0-9]+)|'
    r'(?P<STRING>"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')|'
    r'(?P<OPERATOR>[-+*/]+)|'
    r'(?P<EQUAL>=)|'
    r'(?P<LPAREN>\()|'
    r'(?P<RPAREN>\))|'
    r'(?P<COMMENT>#.*)|'
    r'(?P<WHITESPACE>\s+)'
)
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


def tokenize(code:str):
    tokens = []
    line_number = 1
    line_start = 0
    pos = 0

    for match in re.finditer(token_regex, code):
        if match.start() > pos:
            bad_text = code[pos:match.start()]
            column = match.start() - line_start + 1
            raise SyntaxError(f"Illegal character {bad_text!r} at line {line_number}, column {column}")
        token_type = match.lastgroup
        value = match.group()
        start_pos = match.start()
        column = start_pos - line_start + 1
        if token_type == "WHITESPACE":
            newlines = value.count("\n")
            if newlines > 0:
                line_number += newlines
                line_start = start_pos + value.rfind("\n") + 1
            pos = match.end()
            continue
        if token_type == "NUMBER":
            value = int(value)
        if token_type == "STRING":
            value = value[1:-1]
        if token_type not in ("WHITESPACE", "COMMENT"):
            tokens.append(Token(token_type,value,line_number,column))
        pos = match.end()
    if pos != len(code):
        bad_text = code[pos:]
        column = pos - line_start + 1
        raise SyntaxError(f"Illegal character {bad_text!r} at line {line_number}, column {column}")
    return tokens



class Token:
    def __init__(self, token_type, value, line_number, column):
        self.token_type = token_type
        self.value = value
        self.line_number = line_number
        self.column = column

    def __repr__(self):
        return f"Token({self.token_type!r}, {self.value!r}, line={self.line_number}, column={self.column})"


class VarDeclaration:
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"VarDeclaration(name={self.name}, value={self.value})"

class PrintStatement:
    def __init__(self,expression):
        self.expression = expression
    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"
    
class BinaryOperation:
    def __init__(self,left,operator,right):
        self.left = left
        self.right = right
        self.operator = operator
    def __repr__(self):
        return f"BinaryOperation(left={self.left}, operator={self.operator}, right={self.right})"

class Number:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f"Number(value={self.value})"
    
class Identifier:
    def __init__(self,name):
        self.name = name
    def __repr__(self):
        return f"Identifier(name={self.name})"

class String:
    def __init__(self,value):
        self.value = value
    def __repr__(self):
        return f"String(value={self.value})"
    

class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    def consume(self,expected_type=None):
        token = self.current()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        if expected_type and token.token_type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.token_type} at line {token.line_number}")
        self.pos += 1
        return token
    def parse(self):
        statements = []
        while self.current() is not None:
            stmt = self.parse_statement()
            statements.append(stmt)
        return statements
    def parse_statement(self):
        token = self.current()
        if token.token_type == "VAR":
            return self.parse_var_declaration()
        elif token.token_type == "PRINT":
            return self.parse_print_statement()
        else:
            raise SyntaxError(f"Unexpected token {token.token_type} at line {token.line_number}")
    def parse_var_declaration(self):
        self.consume("VAR")
        ident = self.consume("IDENTIFIER")
        self.consume("EQUAL")
        value = self.parse_expression()
        return VarDeclaration(name=Identifier(ident.value), value=value)

    def parse_print_statement(self):
        self.consume("PRINT")
        expr = self.parse_expression()
        return PrintStatement(expression=expr)
    def parse_factor(self):
        token = self.current()

        if token.token_type == "NUMBER":
            self.consume("NUMBER")
            return Number(token.value)

        elif token.token_type == "STRING":
            self.consume("STRING")
            return String(token.value)

        elif token.token_type == "IDENTIFIER":
            self.consume("IDENTIFIER")
            return Identifier(token.value)

        elif token.token_type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr

        else:
            raise SyntaxError(f"Unexpected token {token.token_type} at line {token.line_number}")
    def parse_term(self):
        left = self.parse_factor()

        while True:
            token = self.current()
            if token and token.token_type == "OPERATOR" and token.value in ("*", "/"):
                op = token.value
                self.consume("OPERATOR")
                right = self.parse_factor()
                left = BinaryOperation(left=left, operator=op, right=right)
            else:
                break

        return left
    def parse_expression(self):
        left = self.parse_term()

        while True:
            token = self.current()
            if token and token.token_type == "OPERATOR" and token.value in ("+", "-"):
                op = token.value
                self.consume("OPERATOR")
                right = self.parse_term()
                left = BinaryOperation(left=left, operator=op, right=right)
            else:
                break

        return left
    

class Interpreter:
    def __init__(self):
        self.environment = {}

    def evaluate(self, node):
        if isinstance(node,Number):
            return node.value
        elif isinstance(node, Identifier):
            name = node.name
            if name in self.environment:
                return self.environment[name]
            else:
                raise NameError(f"Undefined variable '{name}'")
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, BinaryOperation):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)
            if node.operator == "+":
                return left_val + right_val
            elif node.operator == "-":
                return left_val - right_val
            elif node.operator == "*":
                return left_val * right_val
            elif node.operator == "/":
                return left_val / right_val
            else:
                raise RuntimeError(f"Unknown operator {node.operator}")
    def execute(self,node):
        if isinstance(node,VarDeclaration):
            value = self.evaluate(node.value)
            self.environment.update({node.name.name:value})
        elif isinstance(node,PrintStatement):
            value = self.evaluate(node.expression)
            print(value)
    def interpret(self, program):
        for stmt in program:
            self.execute(stmt)

if __name__ == "__main__":
    main()