import time, random, string

def verifyFp():
    def to_base36(value):
        if value == 0:
            return "0"

        alphabet = string.digits + string.ascii_lowercase
        base36 = []

        while value:
            value, rem = divmod(value, 36)
            base36.append(alphabet[rem])

        return ''.join(reversed(base36))

    e = list(string.digits + string.ascii_uppercase + string.ascii_lowercase)
    t = len(e)
    r = to_base36(int(time.time() * 1000))
    n = [None] * 36
    n[8] = n[13] = n[18] = n[23] = "_"
    n[14] = "4"
    for i in range(36):
        if n[i] is None:
            o = int(random.random() * t)
            if i == 19:
                n[i] = e[(o & 3) | 8]
            else:
                n[i] = e[o]
    result = "verify_" + r + "_" + ''.join(n)
    return result



if __name__ == '__main__':

    print(verifyFp())
