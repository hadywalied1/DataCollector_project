import time
import serial as ser
se = ser.Serial(f'COM3', 9600, timeout=1)
start = int(time.time())
while int(time.time()) - start < 15:
    s = se.readline()
    s = s.decode('UTF-8')
    print(s)
    d = s.split(":")

    if d[0] == "Weight":
        d[1] = d[1].strip()
        print(d[1])
    elif d[0] == "Length":
        d[1] = d[1].strip()
        print(d[1])