import re

tokens_types = ["VAR","PRINT","IDENTIFIER","NUMBER","OPERATOR","EQUAL","LPAREN","RPAREN","LBRACE", "RBRACE","COMMENT","IF","ELSE","WHILE","FOR","COMPARISION"]
token_regex = (
    r'(?P<VAR>var)|'
    r'(?P<PRINT>print)|'
    r'(?P<IF>if)|'
    r'(?P<ELSE>else)|'
    r'(?P<WHILE>while)|'
    r'(?P<FOR>for)|'
    r'(?P<COMPARISON>(==|!=|<=|>=|<|>))|'
    r'(?P<IDENTIFIER>[a-zA-Z_][a-zA-Z0-9_]*)|'
    r'(?P<NUMBER>[0-9]+)|'
    r'(?P<STRING>"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')|'
    r'(?P<OPERATOR>[-+*/]+)|'
    r'(?P<EQUAL>=)|'
    r'(?P<LPAREN>\()|'
    r'(?P<RPAREN>\))|'
    r'(?P<LBRACE>\{)|'
    r'(?P<RBRACE>\})|'
    r'(?P<COMMENT>#.*)|'
    r'(?P<WHITESPACE>\s+)'
)


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