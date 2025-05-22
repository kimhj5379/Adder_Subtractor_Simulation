# 4-bit Adder Truth Table Sorter
#.tim file을 읽어들여서 4-bit adder의 진리표를 정렬하고, 누락된 입력 조합을 추가하여 CSV 파일로 저장하는 스크립트입니다.

import csv
import re

input_file = 'full_adder4.tim'
output_file = 'output_truth_table_fixed.csv'

def clean_O_prefix(token):
    return token.replace('$O', '').strip()

def split_tokens(line):
    return [t for t in line.strip().split('\t') if t]

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

header_tokens = split_tokens(lines[0])
header_tokens = [clean_O_prefix(t) for t in header_tokens]
header_tokens = header_tokens[2:]  

desired_header = ['A0','A1','A2','A3','B0','B1','B2','B3','M','S0','S1','S2','S3','Cout']
index_map = [header_tokens.index(h) for h in desired_header]

data_rows = []
for line in lines[1:]:
    tokens = split_tokens(line)
    tokens = [clean_O_prefix(t) for t in tokens]
    tokens = tokens[2:]
    if len(tokens) != len(header_tokens):
        continue
    sorted_row = [tokens[i] for i in index_map]
    data_rows.append(sorted_row)

input_fields = ['A0','A1','A2','A3','B0','B1','B2','B3','M']
input_indices = [desired_header.index(f) for f in input_fields]

unique_rows = []
seen_inputs = set()

for row in data_rows:
    input_key = ''.join([row[i] for i in input_indices])
    if input_key not in seen_inputs:
        seen_inputs.add(input_key)
        unique_rows.append(row)

all_possible_inputs = set(format(i, '09b') for i in range(512))
missing_inputs = all_possible_inputs - seen_inputs

for missing in missing_inputs:
    input_bits = list(missing)
    new_row = ['?'] * len(desired_header)
    for idx, bit in zip(input_indices, input_bits):
        new_row[idx] = bit
    unique_rows.append(new_row)

output_fields = ['Cout', 'S0', 'S1', 'S2', 'S3']
output_indices = [desired_header.index(f) for f in output_fields]

def fill_outputs(row):
    try:
        A_bits = [int(row[desired_header.index(f'A{i}')]) for i in range(4)]
        B_bits = [int(row[desired_header.index(f'B{i}')]) for i in range(4)]
        Cin = int(row[desired_header.index('M')])
    except Exception:
        return row

    A_val = sum(bit << i for i, bit in enumerate(A_bits))
    B_val = sum(bit << i for i, bit in enumerate(B_bits))
    total = A_val + B_val + Cin

    Cout_val = (total >> 4) & 1
    S_vals = [(total >> i) & 1 for i in range(4)]

    row[desired_header.index('Cout')] = str(Cout_val)
    for i in range(4):
        row[desired_header.index(f'S{i}')] = str(S_vals[i])
    return row

for i, row in enumerate(unique_rows):
    unique_rows[i] = fill_outputs(row)

def binary_key(row):
    return int(''.join([row[i] for i in input_indices]), 2)

unique_rows.sort(key=binary_key)

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(desired_header)
    writer.writerows(unique_rows)

print(f"총 {len(unique_rows)}개의 행이 저장되었습니다: '{output_file}'")
