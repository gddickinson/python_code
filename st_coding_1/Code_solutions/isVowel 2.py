def charCount(char):
    char = char.lower()    
    vowel = 'aeiou'    
    for i in vowel:
        if char == i:
            return True
    return False
    
    

print (charCount('a'))
