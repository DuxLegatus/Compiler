from ast_1 import VarDeclaration,Identifier,String,Number,PrintStatement,BinaryOperation,IfStatement,WhileLoop,ForLoop


class Interpreter:
    def __init__(self):
        self.environment = {}

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, String):
            return node.value
        elif isinstance(node, Identifier):
            name = node.name
            if name in self.environment:
                return self.environment[name]
            else:
                raise NameError(f"Undefined variable '{name}'")
        elif isinstance(node, BinaryOperation):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op = node.operator
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    RuntimeError("you cant divide by zero")
                return left / right
            elif op == '==':
                return left == right
            elif op == '!=':
                return left != right
            elif op == '<':
                return left < right
            elif op == '<=':
                return left <= right
            elif op == '>':
                return left > right
            elif op == '>=':
                return left >= right
            else:
                raise RuntimeError(f"Unknown operator: {op}")
        else:
            raise RuntimeError(f"Unknown expression type: {type(node)}")
    def execute(self,node):
        if isinstance(node, VarDeclaration):
            value = self.evaluate(node.value)
            self.environment[node.name.name] = value

        elif isinstance(node, PrintStatement):
            value = self.evaluate(node.expression)
            print(value)

        elif isinstance(node, IfStatement):
            condition = self.evaluate(node.condition)
            if condition:
                for stmt in node.body:
                    self.execute(stmt)
            elif node.else_body:
                for stmt in node.else_body:
                    self.execute(stmt)

        elif isinstance(node, WhileLoop):
            while self.evaluate(node.condition):
                for stmt in node.body:
                    self.execute(stmt)

        elif isinstance(node, ForLoop):
            self.execute(node.init)
            while self.evaluate(node.condition):
                for stmt in node.body:
                    self.execute(stmt)
                self.execute(node.update)

        else:
            raise RuntimeError(f"Unknown statement type: {type(node)}")
    def interpret(self, program):
        for stmt in program:
            self.execute(stmt)