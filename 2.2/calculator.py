"""
Machines are good at crunching numbers - faster and more accurately than most 
humans! Create a small program that calculates something useful to you 
(making you smile is useful). It should take user input, at use at least one of the 
number operators we saw in class: + / * . You may modify one of your previous 
exercises to include calculations, if you wish.

Remember to design your algorithm in English first, then translate it to Python 
code. Test as you go!
"""
#input first number
#input operation
#input second numebr

firstNum = input("Please input the first number: ")
operation = input("Please input the operation: ").strip()
secondNum = input("Please input the second number: ")

match operation:
    case "+":
        final = float(firstNum) + float(secondNum)
    case "-":
        final = float(firstNum) - float(secondNum)
    case "*":
        final = float(firstNum) * float(secondNum)
    case "/":
        if secondNum == 0:
            final = "Undefined"
        else:
            final = float(firstNum) / float(secondNum)
    case "^":
        final = float(firstNum) ** float(secondNum)
    case "%":
        final = float(firstNum) % float(secondNum)   
    case _:
        final = "Invalid Operation"

print(final)
