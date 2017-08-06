def compare_lists(list_a, list_b):
    if list_a == list_b:
        print 'These lists are identical'
    else:
        print 'These lists are not the same'

list_a = [11,6,576,899,34,122]
list_b = [11,6,576,899,34,122]

compare_lists(list_a,list_b)

list_a = [9,6,32,444,91]
list_b = [7,4,1244,289,739]

compare_lists(list_a,list_b)

list_a = ['Carson Wentz', 'Darren Sproles', 'Jason Peters', 'Lane Johnson']
list_b = ['Carson Wentz', 'Legarrette Blount', 'Jason Peters', 'Lane Johnson']

compare_lists(list_a,list_b) 
