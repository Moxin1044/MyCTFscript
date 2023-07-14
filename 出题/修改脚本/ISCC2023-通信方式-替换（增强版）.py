original_text = "QSNCTF{VME50OK?}"
replacement_dict = {
    "幺": "1",
    "两": "2",
    "叁": "3",
    "肆": "4",
    "五": "5",
    "陆": "6",
    "拐": "7",
    "八": "8",
    "勾": "9",
    "洞": "10",
    "可艾": "K",
    "艾一": "A",
    "斯一": "C",
    "艾偶": "L",
    "艾斯": "S",
    "艾福": "F",
    "达不溜": "W",
    "滋一": "Z",
    "艾克斯": "X",
    "科一由": "Q",
    "艾木": "M",
    "之艾": "J",
    "艾吃": "H",
    "啊": "R",
    "比": "B",
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
    "括弧": "{",
    "反括弧": "}",
    "横杠": "-"
}

for key, value in replacement_dict.items():
    original_text = original_text.replace(value, key)

print(original_text)
