import os.path
import pickle
import redis

client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def dump(test_number: int):
    prefix = f"hll_test_{test_number:03d}_user_*"
    dump_data = {}

    for hll_key in client.scan_iter(match=prefix):
        dump_data[hll_key] = client.dump(hll_key)

    dump_file_path = os.path.join(
        "test_dump_files", f"test_{test_number:03d}_rdb_dump.pickle"
    )
    with open(dump_file_path, "wb") as fp:
        pickle.dump(dump_data, fp)


def load(test_number: int):
    dump_file_path = os.path.join(
        "test_dump_files", f"test_{test_number:03d}_rdb_dump.pickle"
    )

    with open(dump_file_path, "rb") as fp:
        dump_data = pickle.load(fp)

    for hll_key, key_dump in dump_data.items():
        client.restore(hll_key, 0, key_dump, replace=True)


def clean_keys(test_number: int | None = None):
    if test_number is None:
        for key in client.keys("*"):
            client.delete(key)
        return

    prefix = f"hll_test_{test_number:03d}_user_*"
    for key in client.keys(pattern=prefix):
        client.delete(key)
