# 4-bit Adder 진리표를 검증하는 스크립트입니다.

import csv

csv_file = 'output_truth_table_fixed.csv'

input_fields = ['A0','A1','A2','A3','B0','B1','B2','B3','M']
output_fields = ['S0','S1','S2','S3','Cout']

with open(csv_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    all_rows = list(reader)

errors = []

for row in all_rows:
    try:
        A_bits = [int(row[f'A{i}']) for i in range(4)]
        B_bits = [int(row[f'B{i}']) for i in range(4)]
        Cin = int(row['M'])

        A_val = sum(bit << i for i, bit in enumerate(A_bits))
        B_val = sum(bit << i for i, bit in enumerate(B_bits))
        total = A_val + B_val + Cin

        expected_S = [(total >> i) & 1 for i in range(4)]
        expected_Cout = (total >> 4) & 1

        actual_S = [int(row[f'S{i}']) for i in range(4)]
        actual_Cout = int(row['Cout'])

        if actual_S != expected_S or actual_Cout != expected_Cout:
            errors.append({
                'inputs': [row[f] for f in input_fields],
                'expected': expected_S + [expected_Cout],
                'actual': actual_S + [actual_Cout]
            })

    except Exception as e:
        errors.append({'row': row, 'error': str(e)})

if errors:
    print(f'⚠️ 총 {len(errors)}개의 오류가 발견되었습니다:')
    for err in errors:
        print('입력:', err['inputs'])
        print('예상 출력:', err['expected'], '| 실제 출력:', err['actual'])
        print('---')
else:
    print('모든 행이 정상적으로 검증되었습니다!')
