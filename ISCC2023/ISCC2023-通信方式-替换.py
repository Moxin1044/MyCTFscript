original_text = "艾艾斯斯一斯一括弧替艾木鸡恩啊艾吃达不溜达不溜鸡达不溜比艾斯危斯一危括弧"
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
    "啊": "A",
    "比": "B",
    "之": "Z",
    "歪": "Y",
    "第": "D",
    "鸡": "J",
    "偶": "O",
    "艾": "I",
    "由": "U",
    "皮": "P",
    "危": "V",
    "替": "T",
    "不": "B",
    "溜": "L",
    "恩": "N",
    "吃": "E",
    "括弧": "{"
}

for key, value in replacement_dict.items():
    original_text = original_text.replace(key, value)

print(original_text)  # 翻转一下最后一个字符不会死
