import ast

a = {}
b = {}
c = 0

with open("d:/Python/portfolio/wallet.txt") as file:
    text = file.readlines()

    position = ast.literal_eval(text[1])
    a.update(position)

    result = ast.literal_eval(text[2])
    b.update(result)

    c = int(text[3])
