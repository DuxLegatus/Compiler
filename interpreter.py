from ast_1 import VarDeclaration,Identifier,String,Number,PrintStatement,BinaryOperation


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