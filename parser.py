from ast_1 import VarDeclaration,Identifier,String,Number,PrintStatement,BinaryOperation


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