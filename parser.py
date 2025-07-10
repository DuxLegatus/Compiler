from ast_1 import VarDeclaration,Identifier,String,Number,PrintStatement,BinaryOperation,IfStatement,WhileLoop,ForLoop


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
        elif token.token_type == "IF":
            return self.parse_if_statement()
        elif token.token_type == "WHILE":
            return self.parse_while_loop()
        elif token.token_type == "FOR":
            return self.parse_for_loop()
        else:
            raise SyntaxError(f"Unexpected token {token.token_type} at line {token.line_number}")
    def parse_block(self):
        statements = []
        self.consume("LBRACE")
        while self.current() and self.current().token_type != "RBRACE":
            statements.append(self.parse_statement())
        self.consume("RBRACE")
        return statements

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
    
    def parse_if_statement(self):
        self.consume("IF")
        condition = self.parse_comparison()
        
        if self.current().token_type == "LBRACE":
            body = self.parse_block()
        else:
            body = [self.parse_statement()]

        else_body = None
        if self.current() and self.current().token_type == "ELSE":
            self.consume("ELSE")
            if self.current().token_type == "LBRACE":
                else_body = self.parse_block()
            else:
                else_body = [self.parse_statement()]
        
        return IfStatement(condition, body, else_body)
    
    def parse_while_loop(self):
        self.consume("WHILE")
        condition = self.parse_comparison()
        if self.current().token_type == "LBRACE":
            body = self.parse_block()
        else:
            body = [self.parse_statement()]
        return WhileLoop(condition, body)
    def parse_assignment(self):
        ident = self.consume("IDENTIFIER")
        self.consume("EQUAL")
        expr = self.parse_expression()

        return VarDeclaration(name=Identifier(ident.value), value=expr)
    def parse_for_loop(self):
        self.consume("FOR")
        init = self.parse_statement()
        condition = self.parse_comparison()
        update = self.parse_assignment()
        if self.current().token_type == "LBRACE":
            body = self.parse_block()
        else:
            body = [self.parse_statement()]
        return ForLoop(init,condition,update, body)
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
    def parse_comparison(self):
        left = self.parse_expression()

        token = self.current()
        if token and token.token_type == "COMPARISON":
            op = token.value
            self.consume("COMPARISON")
            right = self.parse_expression()
            return BinaryOperation(left=left, operator=op, right=right)

        return left
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