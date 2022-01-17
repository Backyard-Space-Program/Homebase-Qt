import sys, datetime
import

def log(*args, file = sys.stdout):
    print(datetime.datetime.now().strftime("[%m/%d/%Y, %H:%M:%S]"), end = ": ", file = file)
    for i in args:
        print(i, end = " ", file = file)
    print("\n", end = "", file = file)
