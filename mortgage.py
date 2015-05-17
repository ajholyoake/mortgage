
import numpy as np
import math


class Mortgage(object):
    def __init__(self,amount,rate,term,end=None):
        if end is None:
            end = term
        self.amount = amount
        self.term = term
        self.rate = rate / 100.0
        self.end = end
        self.parse()

    def parse(self):
        self.rate_m = self.rate / 12
        self.base_repayment = -math.floor((1+self.rate_m)**self.term*self.amount*self.rate_m/(1-(1+self.rate_m)**self.term))

    def loan_remaining(self,n=None,overpayment=0):
        if n is None:
            n = self.end
        r = -(self.base_repayment + overpayment)
        return (1+self.rate_m)**n*(self.amount + r/self.rate_m) - r/self.rate_m

    def interest_paid(self,n=None,overpayment=0):
        if n is None:
            n = self.end
        r = -(self.base_repayment + overpayment)
        amount_left = self.loan_remaining(n,overpayment)
        return -(self.amount + n*r) + amount_left

class House(object):
    def __init__(self,value,rate):
        self.rate = rate/100.0
        self.rate_m = (1+self.rate)**(1/12.0) - 1
        self.initial_value = value

    def value(self,n):
        return self.initial_value * (1+self.rate_m)**n

class Scenario(object):
    def __init__(self,mortgage,house):
        self.mortgage = mortgage
        self.house = house

    def ltv(self,n=None,overpayment=0):
        if n is None:
            n = self.mortgage.end
        return 100*(self.mortgage.loan_remaining(n,overpayment)/self.house.value(n))

    def info(self,n=None,overpayment=0,name=""):
        if n is None:
            n = self.mortgage.end
        N = int(math.ceil(n/12))+1
        m1 = self.mortgage
        h1 = self.house
        s1 = self
        print "\nScenario " + name
        print "loan remaining: " + str([m1.loan_remaining(12*i,overpayment) for i in range(0,N)])
        print "interest paid: "  + str([m1.interest_paid(12*i,overpayment) for i in range(0,N)])
        print "total paid:"      + str([12*i*(m1.base_repayment + overpayment) for i in range(0,N)])
        print "house value  : "  + str([h1.value(12*i) for i in range(0,N)])
        print "loan to value : " + str([s1.ltv(12*i,overpayment) for i in range(0,N)])





m1 = Mortgage(212000,1.65,25*12,2*12)
h1 = House(320000,3)
s1 = Scenario(m1,h1)
s1.info(name="1")


m2 = Mortgage(220000,1.95,25*12,2*12)
s2 = Scenario(m2,h1)
s2.info(overpayment = 200,name="2")


