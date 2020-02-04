import time

t1 = time.time()
t2 = time.time()
while t2 - t1 <= 10:
    print('running')
    t2 = time.time()
print('end')
# print(t1)
