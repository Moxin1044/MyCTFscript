from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 字体文件路径
font_path = 'font/FZSTK.TTF'
# 设置字体和字号
font = ImageFont.truetype(font_path, size=64)
# 设置画布大小
canvas_size = (64, 64)


def draw_char(char):
    # 创建画布和画笔
    im = Image.new('RGB', canvas_size, (255, 255, 255))
    draw = ImageDraw.Draw(im)

    # 在画布中心写字
    bbox = draw.textbbox((0, 0), char, font=font)
    x = (canvas_size[0] - bbox[2] - bbox[0]) // 2 - bbox[0]
    y = (canvas_size[1] - bbox[3] - bbox[1]) // 2 - bbox[1] + 16
    draw.text((x, y), char, font=font, fill=(0, 0, 0))

    # 转换成numpy数组
    im_arr = np.array(im)

    # # 将白色部分变成透明
    # if im_arr.shape[2] == 4:  # 如果有透明通道
    #     im_arr[(im_arr[:,:,0] == 255) & (im_arr[:,:,1] == 255) & (im_arr[:,:,2] == 255)] = [0, 0, 0, 0]
    # else:
    #     im_arr[(im_arr[:,:,0] == 255) & (im_arr[:,:,1] == 255) & (im_arr[:,:,2] == 255)] = [0, 0, 0]

    # 返回Image对象
    return Image.fromarray(im_arr)


if __name__ == '__main__':
    text = input('请输入文本：')

    # 逐个生成每个字的图片，并保存到文件中
    for i, char in enumerate(text):
        char_im = draw_char(char)
        char_im.save(f'output/T2P_{i+1}.png')