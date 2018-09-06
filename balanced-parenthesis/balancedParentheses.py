"""
Balanceador de paréntesis
"""

def balanced(parenthesis):
    stack = []
    for char in parenthesis:
        if len(stack) == 0:
            if char == ")":
                return False
            stack.append(char)
            continue
        peek = stack[len(stack) - 1]
        if char == ")":
            stack.pop()
        else:
            stack.append(char)
    if len(stack) == 0:
        return True
    else:
        return False

if __name__ == '__main__':
    print("True Cases:")
    print(balanced("(())"))
    print(balanced("())"))
    print(balanced("(()"))
    # print(balanced("((((((()))))))"))
    # print("False Cases:")
    # print(balanced("))(("))
    # print(balanced("())()()"))
    # print(balanced(")"))
    # print(balanced("("))