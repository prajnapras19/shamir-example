from Crypto.Util.number import inverse, getPrime, bytes_to_long, long_to_bytes
import random

def f(x0, coeffs, p):
    x = 1
    res = 0
    for c in coeffs:
        res += c * x
        res %= p

        x *= x0
        x %= p
    
    return res

def share(s, n):
    '''
    sharing secret based on shamir secret sharing scheme in GF(p)
    '''
    secret = bytes_to_long(s)
    n_bit = secret.bit_length() + 256 # just for example, using n_bit prime
    p = getPrime(n_bit)
    while p < secret:
        p = getPrime(n_bit)

    k = (n + 1) // 2

    coeffs = [secret]
    for i in range(1, k):
        coeffs.append(random.randint(1, p))

    sharings = []
    for i in range(1, n + 1):
        sharings.append((i, f(i, coeffs, p)))

    return (sharings, p, k)

def getSecret(sharings, p):
    '''
    get back the secret shared by share() function
    '''
    res = 0
    k = len(sharings)
    print('len:', k)
    for j in range(k):
        tmp = sharings[j][1] # y_j
        for m in range(k):
            if m == j:
                continue
            tmp *= sharings[m][0] * inverse(sharings[m][0] - sharings[j][0], p) # x_m / (x_m - x_j)
            tmp %= p
        res += tmp
        res %= p
    return res

print('simulation: share a secret')
secret = b'sebuah rahasia'
n = 5
sharings, p, k = share(secret, n)

print('n:', n)
print('k:', k)
print('prime:', p)
for sharing in sharings:
    print('sharing:', sharing)

print()
print('=' * 50)
print()

print('simulation: get back the secret from the shares')
print('it can be shown that it needs at least k shares to get the secret')

for i in range(n + 1):
    res = getSecret(random.sample(sharings, i), p)
    if i < k:
        print('wrong secret (below threshold k):', long_to_bytes(res))
    else:
        print('secret:', long_to_bytes(res))