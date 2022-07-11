# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 14:30:42 2015

@author: george
"""

balance = 4842
annualInterestRate = 0.2
monthlyPaymentRate = 0.04

####################################s
originalBalance = balance
month = 1
totalPaid =0

def monthBalance(oldBalance, interestRate, PaymentRate):
    monthlyInterestRate = interestRate/12     
    monthlyPayment = PaymentRate * oldBalance
    monthlyPayment = round(monthlyPayment,2)
    unpaidBalance = oldBalance - monthlyPayment
    newBalance = unpaidBalance + (unpaidBalance*monthlyInterestRate)
    newBalance = round(newBalance,2)
    return monthlyPayment, newBalance

while month < 13:
    monthlyPayment, balance = monthBalance(balance, annualInterestRate, monthlyPaymentRate)
    print ("Month: " +str(month))
    print ("Minimum monthly payment: " +str(monthlyPayment))
    print ("Remaining balance: " +str(balance))
    totalPaid = totalPaid + monthlyPayment
    month += 1

#totalPaid = originalBalance - balance
endYearBalance = balance

print ("Total Paid: " +str(totalPaid))
print ("Remaining balance: " +str(endYearBalance))

