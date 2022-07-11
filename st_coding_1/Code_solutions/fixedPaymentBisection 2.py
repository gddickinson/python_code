# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:30:42 2015

@author: george
"""

balance = 999999
annualInterestRate = 0.2


####################################s
originalBalance = balance
epsilon = 0.01

def bisectionPayment (annualInterestRate, balance):
    monthlyInterestRate = annualInterestRate/12
    paymentLow = balance/12
    paymentHigh = (balance*((1+monthlyInterestRate)**12))/12
    payment = (paymentLow+paymentHigh)/2
    #print (payment, balance)
    return payment
     
endYearBalance = balance

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
        month += 1
    return balance
       
while abs(balance) > epsilon:
        #print abs(originalBalance - endYearBalance)
        payment = bisectionPayment(annualInterestRate, balance)    
        balance = yearBalance(balance, annualInterestRate, payment)
        print (payment, balance)
        
print ("Lowest payment: " +str(payment))
