# calculator/pkg/calculator.py

import re


class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 2,
            "-": 2,
            "*": 3,
            "/": 3,
            "(": 1,  # Lower precedence for '(' on stack
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        # Tokenize the expression: split by operators, parentheses, and spaces
        tokens = re.findall(r'(\d+\.?\d*|\+|\-|\*|\/|\(|\))', expression)
        # Filter out empty strings that might result from re.findall with multiple delimiters
        tokens = [token.strip() for token in tokens if token.strip()]
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    self._apply_operator(operators, values)
                if not operators or operators[-1] != '(':
                    raise ValueError("Mismatched parentheses")
                operators.pop()  # Pop '('
            elif token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence.get(operators[-1], 0) >= self.precedence.get(token, 0)
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            if operators[-1] == '(':
                raise ValueError("Mismatched parentheses")
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
