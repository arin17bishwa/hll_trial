import json
import os.path

import redis
from itertools import batched
from test_rdb_00 import load, dump, clean_keys
from test_config_00 import TEST_NO
from test_file_generator_00 import get_part_numbers
client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def verify_pickle_load(test_number: int):
    test_data_file_path = os.path.join(
        "test_result_files", f"userdata_test_{test_number:03d}.json"
    )

    with open(test_data_file_path) as fp:
        test_data = json.load(fp)
    verification_data = {}
    for hll_key, user_data in test_data.items():
        new_est_cnt = client.pfcount(hll_key)
        old_est_cnt = user_data["estimate"]
        actual_cnt = user_data["actual"]
        # print(hll_key, old_est_cnt, new_est_cnt, actual_cnt)
        assert old_est_cnt == new_est_cnt
        verification_data[hll_key] = {
            "count": actual_cnt,
            "post_load_estimate": new_est_cnt,
        }
    load_result_file_path = os.path.join(
        "test_load_result_files",
        f"userdata_test_post_load_result_{test_number:03d}.json",
    )
    with open(load_result_file_path, "w") as fp:
        json.dump(verification_data, fp, indent=4)


def insert_all_parts():
    hll_key='hll_all_parts_key_000'
    items=get_part_numbers()
    for batch in batched(items, 100):
        client.pfadd(hll_key, *batch)

    est=client.pfcount(hll_key)
    print(est)
    return est


def main():
    pass
if __name__ == "__main__":
    main()
    # clean_keys()
    # dump(2)
    # load(10)
    # verify_pickle_load(10)
