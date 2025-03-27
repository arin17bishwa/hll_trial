import json
import os.path
from itertools import batched
from test_rdb_00 import dump

import redis

from test_config_00 import TEST_NO


client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def func(test_data: dict) -> dict:
    test_result_obj = {}

    for hll_key, test_user_data in test_data.items():
        for batch in batched(test_user_data["items"], 1000):
            client.pfadd(hll_key, *batch)
        est_cnt = client.pfcount(hll_key)
        test_result_obj[hll_key] = {
            "actual": test_user_data["count"],
            "estimate": est_cnt,
        }

    return test_result_obj


def main():
    test_data_file_path = os.path.join(
        "test_data_files", f"userdata_test_{TEST_NO:03d}.json"
    )
    with open(test_data_file_path) as fp:
        test_data = json.load(fp)

    test_result = func(test_data)

    test_result_file_path = os.path.join(
        "test_result_files", f"userdata_test_{TEST_NO:03d}.json"
    )
    with open(test_result_file_path, "w") as fp:
        json.dump(test_result, fp, indent=4)

    return





if __name__ == "__main__":
    main()
    dump(test_number=TEST_NO)
    client.close()
