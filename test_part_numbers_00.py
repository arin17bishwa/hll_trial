"""for continuous testing with ~180k part numbers"""

import json, os, redis

from black.lines import enumerate_reversed

client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def get_part_numbers(path: str = "log_parsing/part_numbers_01.json") -> list[str]:
    with open(path) as fp:
        data = json.load(fp)
    return data["part_numbers"]


def func():
    test_user_key = "hll_180k_parts_test_000"
    _=client.delete(test_user_key)
    parts = get_part_numbers()
    metrics: list[dict] = []

    for idx, part_number in enumerate(parts, start=1):
        _ = client.pfadd(test_user_key, part_number)
        est_cnt = client.pfcount(test_user_key)
        diff = abs(est_cnt - idx)
        metrics.append(
            {
                "part_number": part_number,
                "actual_count": idx,
                "estimated_count": est_cnt,
                "percent_diff": round((diff*100)/idx,5),
            }
        )

    with open("test_result_files/continuous_test_data_180k_00.json", "w") as fp:
        json.dump(metrics, fp, indent=4)
    return metrics


def main():
    func()


if __name__ == "__main__":
    main()
