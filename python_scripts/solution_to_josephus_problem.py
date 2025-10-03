#!/usr/bin/env python

def power_check(number, base) :
    ''' This function checks if the number 
    is a perfect number if base is raised to some
    power, finds that power,
    for example lets say number given to this function
    is 10 it will return 2, because 2^3 = 8
    it finds the power(3) and subtracts it from the original
    number i.e. 10 - (2)^3, returning the left,
    this function is to solve Josephus problem for some
    number of people and the turn of people to kill, 
    this approach inspired from Numberphile's video on the 
    topic . '''
    
    original_number = number
    power = 0
    while number > 1 :
        number //= base
        power += 1
    
    perfect_number = base**power
    left_number = original_number - perfect_number
    return (left_number)

def josephus_solution(number, base=2) :
    left = power_check(number, base)
    if left == 0 :
        return (1)
    else :
        return ((base*left) + 1)

number_of_people = int(input(" Please input the total number of people : \n "))
found = josephus_solution(number_of_people)

print(f" For {number_of_people} people the winner would be {found} ")
print(f" alongwith number of people, you can specify the number of people to skipped for killing in the script ")
