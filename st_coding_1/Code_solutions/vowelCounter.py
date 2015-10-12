s = 'str'
ans = 0
def charCount(vowel, string):
    char = string.count(vowel)
    return char
a = charCount('a',s)
e = charCount('e', s)
i = charCount('i', s)
o = charCount('o', s)
u = charCount('u', s)
ans = a+e+i+o+u
print ("Number of vowels: " +str(ans))

