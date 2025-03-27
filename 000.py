import redis
client = redis.Redis(host='localhost', port=6379, decode_responses=True)


def func():
    cnt=client.pfcount('hll_key')
    print(cnt)

    all_keys = client.keys("*")
    hll_keys = [key for key in all_keys if client.type(key) == "hyperloglog"]
    print("HyperLogLog keys:", all_keys)


if __name__=='__main__':
    func()
    client.close()
