import random
import time


def randTime(x, y, z, f_digit, s_digit, t_digit):  # sleeps in  miliseconds from fdigit.sdigit+tdigit+random
    """x, y, z are the minimum millisecs"""
    """fdigit, etc. are maximum values"""
    # global timer

    random.seed()
    n = random.random()
    n = str(n)
    n = n[2:]

    f_digit = str(random.randint(x, f_digit))
    s_digit = str(random.randint(y, s_digit))
    t_digit = str(random.randint(z, t_digit))

    milisecs = f_digit + '.' + s_digit + t_digit + n
    milisecs = float(milisecs)
    # print milisecs
    # print("waiting {}".format(milisecs))
    # timer += milisecs
    time.sleep(milisecs)


# TODO
# a better RAND TIME functions

# milsecionds
def randomTime(start, end):
    seconds = float(random.randint(start, end)) / 1000
    print("Delay %s seconds" % seconds)
    time.sleep(seconds)
