import redis
from itertools import batched

# Connect to Redis
client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def test_hyperloglog_accuracy(n_values):
    """
    Tests Redis HyperLogLog accuracy for different values of n.

    Args:
        n_values (list): List of different n values to test.
    """
    key = "hll_test"  # Redis HyperLogLog key

    for n in n_values:
        # Clear previous data
        client.delete(key)

        # Insert n elements into HyperLogLog in batches
        for batch in batched(range(n), 100):
            client.pfadd(key, *batch)

        # Get estimated count from Redis
        est_cnt = client.pfcount(key)

        # Calculate error percentage
        difference = abs(est_cnt - n)
        error_percentage = (difference * 100) / n

        # Print results
        print(f"Actual Count: {n}, Estimated Count: {est_cnt}, Error: {error_percentage:.6f}%")


if __name__ == '__main__':
    # Test for different n values
    arr = [100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
    test_hyperloglog_accuracy(arr)
