#Write a program that takes a list and prints a message for each element in the list, based on that element's data type.

#Your program input will always be a list. For each item in the list, test its data type. If the item is a string, concatenate it onto a new string. 
#If it is a number, add it to a running sum. At the end of your program print the string, the number and an analysis of what the list contains. 
#If it contains only one type, print that type, otherwise, print 'mixed'.

mixed_list = ['Carson Wentz', 11, 'Jason Peters', 91, 'Malcolm Jenkins', 27]
string_list = ['Washington', 'Philadelphia', 'New York', 'Dallas']
integer_list = [.531, .438, .688, .813]

def list_type():
    new_string = ''
    total = 0

    for value in :
        if isinstance(value, int) ir isinstance(value, float):
            total += value
        elif isinstance(value, str):
            new_string += value

    if new_string and total:
        print 'The list you made is of a mixed type'
        print 'string:', new_string
        print 'total:', total

    elif new_string:
        print 'The list you made is of a string type'
        print 'String:', new_string

    else:
        print 'The list you made is of a numbered or integer tpye'
        print 'total:', total

print list_type(mixed_list)
print list_type(string_list)
print list_type(integer_list)

