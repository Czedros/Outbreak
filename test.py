from random import Random
import random
a = Random()
a.seed(10)
randCount = 0
for i in range(random.randint(0, 10)):
    randCount += 2
    a.randint(0, 100)
    a.randint(0, 100)

b = Random()
print(a.getstate())
b.setstate(a.getstate())
print(a.randint(0, 10))
print(b.randint(0, 10))