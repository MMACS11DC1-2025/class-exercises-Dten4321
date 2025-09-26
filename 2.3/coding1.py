"""
Write an Age in 2056 program that asks your age and outputs how old you'll be 31 years from now.

Examples:

How old are you?
> 10
In 2056, you will be 41 years old!
--
How old are you?
> 25
In 2056, you will be 56 years old!
"""
import datetime

print("How old are you?")
age = int(input("> "))
currentYear = datetime.datetime.now().year
newAge = age + (2056 - currentYear)
print(f"In In 2056, you will be {newAge} years old!")
