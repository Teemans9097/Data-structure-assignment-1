class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


if __name__ == "__main__":
    stack = Stack()

    stack.push(10)
    stack.push(20)
    stack.push(30)

    print("Top item:", stack.peek())
    print("Removed item:", stack.pop())
    print("New top item:", stack.peek())
    print("Is the stack empty?", stack.is_empty())


def precedence(operator):
    if operator in ("+", "-"):
        return 1
    if operator in ("*", "/"):
        return 2
    return 0


def apply_operator(left, right, operator):
    if operator == "+":
        return left + right
    if operator == "-":
        return left - right
    if operator == "*":
        return left * right
    if operator == "/":
        if right == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return left / right

    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_expression(expression):
    import re

    numbers = Stack()
    operators = Stack()

    # Split the expression into numbers, operators, and parentheses.
    compact = re.sub(r"\s+", "", expression)
    tokens = re.findall(r"\d+(?:\.\d+)?|[()+*/-]", compact)

    if not tokens or "".join(tokens) != compact:
        raise ValueError("Empty expression or invalid characters.")

    def calculate_top():
        if len(numbers.items) < 2:
            raise ValueError("An operator is missing a number.")

        right = numbers.pop()
        left = numbers.pop()
        operator = operators.pop()

        result = apply_operator(left, right, operator)
        numbers.push(result)

    expecting_number = True

    for token in tokens:
        if token[0].isdigit():
            if not expecting_number:
                raise ValueError("Missing operator between numbers.")

            value = float(token) if "." in token else int(token)
            numbers.push(value)
            expecting_number = False

        elif token == "(":
            if not expecting_number:
                raise ValueError("Missing operator before '('.")

            operators.push(token)

        elif token == ")":
            if expecting_number:
                raise ValueError("Missing number before ')'.")

            while not operators.is_empty() and operators.peek() != "(":
                calculate_top()

            if operators.is_empty():
                raise ValueError("Unmatched closing parenthesis.")

            operators.pop()
            expecting_number = False

        else:
            if expecting_number:
                raise ValueError("Expected a number or '('.")

            while (
                not operators.is_empty()
                and operators.peek() != "("
                and precedence(operators.peek()) >= precedence(token)
            ):
                calculate_top()

            operators.push(token)
            expecting_number = True

    if expecting_number:
        raise ValueError("Expression ends without a number.")

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError("Unmatched opening parenthesis.")

        calculate_top()

    if len(numbers.items) != 1:
        raise ValueError("Invalid expression.")

    return numbers.pop()
