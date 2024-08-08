import pandas as pd


def process_xlsx_to_txt(xlsx_path, txt_path, column_name='第二列'):
    df = pd.read_excel(xlsx_path)
    column_data = df[column_name]

    with open(txt_path, 'w', encoding='utf-8') as f:
        for value in column_data:
            # 确保值不是NaN
            if pd.notna(value):
                value_str = str(value)

                if value_str.startswith('http://') or value_str.startswith('https://'):
                    value_str = value_str[value_str.find('//') + 2:]
                parts = value_str.split('/', 1)  # 第二个参数限制分割次数为1
                if len(parts) > 1:
                    processed_value = parts[0]
                else:
                    processed_value = value_str
                f.write(processed_value + '\n')


process_xlsx_to_txt('信阳.xlsx', 'output.txt', '网站域名')
