s = 'strbobobbobobbbbobbobbobobdsgrea'
ans = 0
word = 'bob'
wordLength=len(word)
start=0
end=len(s)
stringLength=len(s)

while start < stringLength:
    if (s.count(word,start,start+wordLength)) == 1:
        ans += 1
    start += 1

print ("Number of times bob occurs is: " +str(ans))

