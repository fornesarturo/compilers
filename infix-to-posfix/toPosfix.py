def infixToPosfix(expr):
    print(expr)
    result = ""
    stack = []
    order = { "+": 1, "-": 1, "*": 2, "/": 2, "^": 3 }
    wait = 0
    for c in expr:
        print()
        print("EI: ",c)
        print("EP: ", result)
        print("STACK: ", stack)
        if c.isdigit():
            result += c + " "
            continue
        else:
            if len(stack) == 0:
                stack.append(c)
                continue
            top = stack[-1]
            if order[c] > order[top]:
                stack.append(c)
                continue
            if order[c] == order[top]:
                result+=stack.pop() + " "
                stack.append(c)
                continue
            if order[c] < order[top]:
                while len(stack) > 0:
                    result+=stack.pop() + " "
                    if len(stack) > 0 and order[c] > order[stack[-1]]:
                        break
                stack.append(c)
    while (len(stack) > 0):
        result += stack.pop() + " "
    return result

expression = "2+3*4-6^1/2"
# 2 3 4 * + 6 1 ^ 2 / -
print(infixToPosfix(expression))