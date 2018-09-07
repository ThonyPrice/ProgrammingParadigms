# Pyhton script for generating database of 500 persons

number = 500

for n in range (number):
    print("person(", n, ")", ".", sep='')
    
for n in range (1, number):
    if n % 3 != 0:
        print("knows(", 0, ",", n, ")", ".", sep='')
    if n % 3 == 0:
        print("knows(", n, ",", n-1, ")", ".", sep='')
        print("knows(", n, ",", n-2, ")", ".", sep='')
        

    
