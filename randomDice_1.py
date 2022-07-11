#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 19:41:08 2022

@author: george
"""

import numpy as np

primes = [2, 3, 5, 7, 11]

numberOfRolls = 10000

# 2 x 2 array of ints
diceRoll= np.random.random_integers(1, 6, size=(2, numberOfRolls))

#sum dice
sumDice = diceRoll[0] + diceRoll[1]

#check prime
numberPrimes = 0
for prime in primes:
    numberPrimes += np.count_nonzero(sumDice == prime)

#check equals
numberEquals = 0

for i in range(len(diceRoll[1])):
    #print (diceRoll[0][i], diceRoll[1][i])
    if diceRoll[0][i] == diceRoll[1][i]:
        #print ('equal')
        numberEquals += 1

#payout
primePayout = numberPrimes * 1
equalsPayout = numberEquals * 3

print ('prime payout = {}'.format(primePayout))
print ('equals payout = {}'.format(equalsPayout))
