from ft import ftclient
import time

f = ftclient()

black_real = (1,1,1)

for col in range(45):
    for row in range(35):
        f.set(col, row, black_real)
while True:
    f.show()
    time.sleep(0.5)
