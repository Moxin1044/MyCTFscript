import cv2
from pyzbar.pyzbar import decode

def scan_qr_code(image_path):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"无法加载图片: {image_path}")
        return

    # 解码二维码
    decoded_objects = decode(img)
    if not decoded_objects:
        print("未检测到二维码。")
        return

    # 输出二维码内容
    for obj in decoded_objects:
        print(f"类型: {obj.type}")
        print(f"数据: {obj.data.decode('utf-8')}")
        print("-" * 30)

if __name__ == "__main__":
    scan_qr_code("modified.png")
