with open("data.txt", "w") as file:
    file.write("Python")

with open("data.txt", "a") as file:
    file.write("\nWorld")

with open("data.txt", "r") as file:
    content = file.read()

print(content)

with open("data.txt", "r") as file:
    lines = file.readlines()

print(lines)

def read_products(filename):
  lis = []
  with open(filename, "r") as file:

    for line in file:
        

        stripped = line.strip()

        lis.append(stripped)

    return lis

result= read_products("data.txt")
print(result)

products = ["Laptop", "Mouse", "Keyboard"]
def save_products(filename, products):
   with open(filename, "w") as file:
    for product in products:
        file.write(product + "\n")

    return products
        

prod = save_products("data.txt",products)
print(prod)