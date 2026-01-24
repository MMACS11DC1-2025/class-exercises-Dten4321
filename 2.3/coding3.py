"""
Write a McDoland's program that takes your order and outputs the total cost.

It first asks if you want a burger for $5. It then asks if you want fries for $3. It outputs the total with 14% tax.

The program should accept Yes/No or yes/no.

Example:

Would you like a burger for $5? (Yes/No)
> yes
Would you like fries for $3? (Yes/No)
> yes
Your total is $9.12

Would you like a burger for $5? (Yes/No)
> yes
Would you like fries for $3? (Yes/No)
> no
Your total is $5.699999999999999

Would you like a burger for $5? (Yes/No)
> no
Would you like fries for $3? (Yes/No)
> yes
Your total is $3.42
"""

print("Would you like a burger for $5? (Yes/No)")
burger = input("> ").lower()
if burger == "yes":
    burger = float(5)
else:
    burger = float(0)

print("Would you like fries for $3? (Yes/No)")
fries = input("> ").lower()
if fries == "yes":
    fries = float(3)
else:
    fries = float(0)

total = (burger + fries) * 1.14
print(f"Your total is ${total}")