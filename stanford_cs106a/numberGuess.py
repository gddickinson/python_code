print ("Please think of a number between 0 and 100!")
x = 100
ans = 0
low = 0
high = x
ans = (high + low)/2
user_input = ''

while user_input != 'c':
    
    print ("Is your secret number " + str(ans) + "?")
    user_input = raw_input("Enter 'h' to indicate the guess is too high. Enter 'l' to indicate the guess is too low. Enter 'c' to indicate I guessed correctly.")
    
    if user_input == 'h':
        high = ans
    elif user_input == 'l':
        low = ans
    elif user_input =='c':
        break
    else:
        print ("Sorry I did not understand your input")
    
    ans = (high + low)/2
    
print ("Game over. Your secret number was: " +str(ans))
