from time import time

def stopwatch(fn):
    def decorated(*args, **kwargs):
        t0 = time()
        res = fn(*args, **kwargs)
        return (time()-t0, res)
    return decorated

def gcd(a, b):
    while b != 0:
       a, b = b, a % b
    return a

def test():
    decorated_gcd = stopwatch(gcd)
    delta, res = decorated_gcd(1989, 867)
    assert delta > 0
    assert res == 51

if __name__=='__main__':

    n1 = 99971 * 99989
    n2 = 99971 * 99991

    print stopwatch(gcd)(9949 * 9967, 9949 * 9973)
