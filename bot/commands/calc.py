from bot.base import Command

# We are not using 'eval' or any kind of bult-in function.
# We are handcrafting a calculator.

# Go to line 138 for the command definition itself.


class Calculator:
    valid_chars = ('+', '-', '*', '/', '(', ')', ' ', '\t') 
    
    def __init__(self, src):
        # Initializes a calculator with the source "code"
        self.idx = 0
        self.src = src
        # Hope 'src' is not an empty string
        self.char = self.src[self.idx]

    def is_at_end(self):
        return self.idx >= len(self.src)

    def advance(self):
        self.idx += 1
        # If we reached the end we set self.char to None.
        self.char = self.src[self.idx] if not self.is_at_end() else None

        # Recursively call advance to advance one more time
        # if there is a space.
        if self.char == " ":
            self.advance()

    def error(self):
        error_msg = self.src + "\n"
        # Add the ^-- thing
        error_msg += " " * self.idx + "^-- Here."
        raise RuntimeError(error_msg)

    def number(self):
        # Store it as a string
        num_str = ""
        while not self.is_at_end() and self.char.isdigit() or self.char == ".":
            num_str += self.char
            self.advance()

        # Try to return it
        try:
            return float(num_str)
        except ValueError:
            # Error converting the string - invalid number
            self.error()

    # Recursive descent parsing
    def expr(self):
        # expr takes care of addition and subtraction.
        # Its precedence is 'AS' in 'PEMDAS'.
        # Left operand
        left = self.term()

        while self.char in ("+", "-"):
            op = self.char
            # Advance past the operator
            self.advance()
            right = self.term()

            # Add them if op == '+', subtract them otherwise
            left = left + right if op == "+" else left - right

        return left

    def term(self):
        # term takes care of multiplication and division.
        # Its precedence is 'MD' in 'PEMDAS'.
        left = self.factor()

        while self.char in ("*", "/"):
            op = self.char
            # Advance past the operator
            self.advance()
            right = self.factor()

            # multiply them if op == '*', divide them otherwise
            left = left * right if op == "*" else left / right

        return left

    def factor(self):
        # Unary operators
        if self.char in ("+", "-"):
            op = self.char
            self.advance()
            # Recursively call factor
            child = self.factor()

            return -child if op == "-" else child

        # Else, it must be a call expression.
        # "1+4(9-9)"
        return self.call()

    def call(self):
        expr = self.literal()

        while True:
            # Ι δοη'τ τςιηκ τςιξ ιξ νεπυ πεθεναη
            # Oh sorry wrong keyboard.
            # Using "while True" here because we also
            # want to allow things such as 2(9)(8)
            if self.char == "(":
                self.advance()
                right_expr = self.expr()
                if self.char != ")":
                    self.error()

                self.advance()
                expr = expr * right_expr

            else:
                # There might be a nasty bug here.
                # An example is: 2a2
                # This little expression is invalid, but it sneakily 
                # gets past validity checks in our beloved calculator.
                # The issue is here. We should handle this case gracefully
                # by checking if the current character we are on is valid.
                if self.char is None \
                   or self.char.isdigit() or self.char in self.valid_chars:

                    # Allow it
                    break

                else:
                    # There you are, you disgruntled monster!
                    self.error()

        return expr

    def literal(self):
        # If we have a number, return it
        if self.char.isdigit():
            return self.number()

        if self.char == "(":
            # Parenthised expression.
            # Skip the '('
            self.advance()
            expr = self.expr()
            # Check for ')'
            if self.char != ")":
                self.error()

            self.advance()
            return expr

        self.error()


class cmd(Command):
    # The command.
    name = "calc"
    usage = "calc <*expression>"
    description = "Calculates the given expression and sends the result. Valid operators are: +, -, /, *, and ()."

    async def execute(self, arguments, message) -> None:
        # First smush all arguments into one in order to
        # have a valid expression. We don't want to throw
        # an error if the user typed "1 + 1" instead of "1+1".
        # (Argument parsing stuff)
        expression = " ".join(arguments)

        # Create a calculator instance.
        calculator = Calculator(expression)

        # Get the result.
        result = calculator.expr()

        expression = expression.translate(
            str.maketrans({"*": "\\*"})
        )  # escape '*' characters in expression

        # Send the result:
        await message.channel.send(f"_{expression}_ = **{result:g}**")


# Terminal testcase
if __name__ == '__main__':
    print("calc.py command terminal testcase. Press ^C to quit.")
    while True:
        expression = input('>> ')
        # The thing that will calculate our expression:
        calculator = Calculator(expression)

        # Avoid terminating if an error is encountered
        result = None
        try:
            result = calculator.expr()
        except Exception as e:
            print(f"An error occured: \n{e}")
        
        print(f"=> {result}")

