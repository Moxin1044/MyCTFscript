original_text = "艾艾斯斯一斯一括弧艾木啊艾替艾木歪艾歪恩达不溜比艾福偶第艾偶括弧"
replacement_dict = {
    "可艾": "K",
    "斯一": "C",
    "艾偶": "L",
    "艾斯": "S",
    "艾福": "F",
    "达不溜": "W",
    "滋一": "Z",
    "艾克斯": "X",
    "科一由": "Q",
    "艾木": "M",
    "艾吃": "H",
    "啊": "R",
    "比": "B",
    "之": "Z",
    "歪": "Y",
    "第": "D",
    "易": "E",
    "鸡": "G",
    "偶": "O",
    "艾": "I",
    "由": "U",
    "皮": "P",
    "危": "V",
    "替": "T",
    "不": "B",
    "溜": "L",
    "恩": "N",
    "括弧": "{"
}

for key, value in replacement_dict.items():
    original_text = original_text.replace(key, value)

print(original_text)  # 翻转一下最后一个字符不会死
