# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:30:42 2015

@author: george
"""

balance = 392600
annualInterestRate = 0.2


####################################s
originalBalance = balance
#month = 1
payment = 0.000001
originalPayment = payment
endYearBalance = balance
#epsilon = 10


def monthBalance(oldBalance, interestRate, PaymentRate):
    monthlyInterestRate = interestRate/12     
    monthlyPayment = PaymentRate
    monthlyPayment = round(monthlyPayment,2)
    unpaidBalance = oldBalance - payment
    newBalance = unpaidBalance + (unpaidBalance*monthlyInterestRate)
    newBalance = round(newBalance,2)
    #print (newBalance)
    return newBalance
 
def yearBalance(balance, annualInterestRate, payment): 
    month =1
    while month < 13:
        balance = monthBalance(balance, annualInterestRate, payment)
        #print (payment, balance)
        if balance <= 0:
            return balance
        month += 1
    return balance
       
while endYearBalance > 0:    
        endYearBalance = yearBalance(balance, annualInterestRate, payment)    
        payment += 10


print ("Lowest payment: " +str(payment-originalPayment))
#print ("Remaining balance: " +str(endYearBalance))

