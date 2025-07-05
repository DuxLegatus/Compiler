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