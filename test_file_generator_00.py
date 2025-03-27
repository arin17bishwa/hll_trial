import json
import os
import random

from test_config_00 import TEST_NO

NUM_PARTS:int=10_000

def get_part_numbers(sample_size:int|None=None):
    if sample_size is None:
        sample_size=NUM_PARTS
    with open(os.path.join('test_part_data','part_numbers_00.json')) as fp:
        obj=json.load(fp)
    return obj['part_numbers'][:sample_size]

def func()->dict:
    final_obj={}
    sample_parts_data=get_part_numbers(2)
    for user_no in range(NUM_USERS):
        username=f'hll_test_{TEST_NO:03d}_user_{user_no:06d}'
        item_cnt=random.randint(1,min(NUM_PARTS, len(sample_parts_data)))
        items=random.sample(sample_parts_data, item_cnt)
        final_obj[username]={'count':item_cnt, 'items':items}
    return final_obj

def main():
    test_file_name=f'userdata_test_{TEST_NO:03d}.json'
    test_file_path=os.path.join('test_data_files',test_file_name)
    if os.path.exists(test_file_path):
        raise Exception('Test file exists. Increase test serial number.')
    test_data=func()
    with open(test_file_path,'w') as fp:
        json.dump(test_data, fp, indent=4)

if __name__ == '__main__':
    NUM_USERS=100_000
    main()