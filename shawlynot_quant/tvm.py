from math import exp

def future_discrete_value(present_value, rate, number_periods):
    return present_value*(1+rate)**number_periods

def present_discrete_value(future_value, rate, number_periods):
    return future_value*(1+rate)**-number_periods

def future_continuous_value(present_value, rate, time):
    return present_value*exp(r*t)

def present_continuous_value(future_value, rate, time):
    return present_value*exp(-r*t)