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
    
class IfStatement:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        return f"IfStatement(condition={self.condition}, body={self.body}, else_body={self.else_body})"

class WhileLoop:
    def __init__(self, condition, body):
        self.condition = condition 
        self.body = body     
    def __repr__(self):
        return f"WhileLoop(condition={self.condition}, body={self.body})"


class ForLoop:
    def __init__(self, init, condition, update, body):
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body  

    def __repr__(self):
        return f"ForLoop(init={self.init}, condition={self.condition}, update={self.update}, body={self.body})"


