import math


for i in range(1, 51):
    if i % 4 == 0:
        continue
    if i == 25:
        break
    
    is_prime = True
    if i > 1:
        for j in range(2, int(math.sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break

    if is_prime and i > 1:
        print(i)
