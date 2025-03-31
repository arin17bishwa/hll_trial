import json
import os
import re
import logging

from Logging import setup_logger

logger=setup_logger()

from hll_log_files.log_chucker import get_line_stream

base_log_path='hll_log_files'

def main():
    sm=0
    for line in get_line_stream():
        sm+=1

    print(sm)

def line_parser()->list[str]:
    part_numbers=[]
    part_indices=[]
    line_regex=r".*\[http-nio-8081-exec-1\] INFO  c.t.a.v.a.s.i.CrossConsumptionHllServiceImpl - actual count = (?P<number>\d*), part = (?P<part_name>.*), estimated .*"
    compiled_regex=re.compile(line_regex)
    for line_idx, line in enumerate(get_line_stream(), start=1):
        match=re.match(pattern=compiled_regex, string=line)
        if match:
            part_name=match.groupdict().get('part_name')
            part_idx=match.groupdict().get('number')
            logger.debug(f"part_idx: |{part_idx}| || part_name: |{part_name}|")
            if part_name:
                part_numbers.append(part_name)
                part_indices.append(part_idx)

            # break
    return part_numbers, part_indices

def func():
    part_numbers, part_indices=line_parser()
    print(len(part_numbers))
    with open('part_numbers_01.json','w') as fp:
        json.dump({'part_numbers':part_numbers}, fp, indent=4)

    with open('part_indices_01.json','w') as fp:
        json.dump(sorted(map(int, part_indices)), fp, indent=4)
    return


if __name__ == '__main__':
    func()