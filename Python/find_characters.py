
#Write a program that takes a list of strings and a string containing a single character, and prints a new list of all the strings containing that character.

z_fighters_list = ['goku', 'gohan', 'piccolo', 'trunks', 'vegeta', 'krillin', 'tien', 'yamcha', 'bulma']
frieza_killed = 'a'

for item in z_fighters_list:
    if item.find('a') != -1:
        print item