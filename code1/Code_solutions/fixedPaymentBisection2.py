# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 09:02:23 2015

@author: george
"""

balance = 999999
annualInterestRate = 0.18


####################################s
originalBalance = balance
epsilon = 0.05


def monthBalance(oldBalance, interestRate, payment):
    monthlyInterestRate = interestRate/12     
    monthlyPayment = payment
    monthlyPayment = round(monthlyPayment,3)
    unpaidBalance = oldBalance - monthlyPayment
    newBalance = unpaidBalance + (unpaidBalance*monthlyInterestRate)
    newBalance = round(newBalance,3)
    #print (newBalance)
    return newBalance
 
def yearBalance(balance, annualInterestRate, payment): 
    month =1
    while month < 13:
        balance = monthBalance(balance, annualInterestRate, payment)
        #print (payment, balance)
        month += 1
    return balance


def findPayment(balance, annualInterestRate, epsilion):
    monthlyInterestRate = annualInterestRate/12
    originalBalance = balance    
    paymentLow = balance/12
    paymentHigh = (balance*((1+monthlyInterestRate)**12))/12
    payment = (paymentLow+paymentHigh)/2
    while abs(balance) > epsilon:
        balance = yearBalance(originalBalance, annualInterestRate, payment)
        #print("Balance" +str(balance))        
        if balance > epsilon:
            paymentLow = payment
            paymentHigh = paymentHigh
        else:
            paymentLow = paymentLow
            paymentHigh = payment
        payment = (paymentLow+paymentHigh)/2
    return payment

lowestPayment = round(findPayment(originalBalance, annualInterestRate, epsilon),2)

print ("Lowest Payment: " +str(lowestPayment))


        
        
        
