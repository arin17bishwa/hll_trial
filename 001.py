import random
from itertools import batched
from math import acosh
from threading import activeCount

import redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)
key="hll_key_001_000"

def func(n:int)->float:
    print(f'actual cnt= {n}')
    for batch in batched(range(n), 10):
        client.pfadd(key,*batch)
    est_cnt=client.pfcount(key)
    print(f'est cnt= {est_cnt}')

    difference=abs(est_cnt-n)
    error_percent=(difference*100)/(n+0)
    print(f'change %: {error_percent:.4f}%')

    client.delete(key)
    return error_percent

def main():
    iterations=10
    mx_int=100_000
    error_percents=[]
    for idx in range(1,iterations+1):
        n=random.randint(1,mx_int)
        error_percent=func(n)
        error_percents.append(error_percent)
        print('='*90)


    keys=client.keys('*')
    print(keys)
    print()
    print('max error: ',max(error_percents))


if __name__=='__main__':
    main()
    client.close()
