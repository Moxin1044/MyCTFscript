#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精确二维码修复工具 - 基于分析结果
使用11px模块大小进行精确修复
"""

import cv2
import numpy as np
from pyzbar import pyzbar
import os


def create_precise_qr_repair(image_path):
    """基于分析结果进行精确修复"""
    # 读取图像
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 图像已经是完美二值化的
    binary = gray.copy()

    print("开始精确修复...")
    print("基于分析结果: 模块大小=11px")

    # 扩展的QR码配置 - 更多版本和模块大小
    qr_configs = []

    # 生成更全面的配置组合
    versions_and_modules = [
        (1, 21), (2, 25), (3, 29), (4, 33), (5, 37), (6, 41), (7, 45), (8, 49),
        (9, 53), (10, 57), (11, 61), (12, 65), (13, 69), (14, 73), (15, 77)
    ]

    # 扩展模块大小范围 (基于分析结果11px，但允许更大范围)
    module_sizes = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    print(f"生成配置组合: {len(versions_and_modules)} 版本 × {len(module_sizes)} 模块大小")

    # 生成所有可能的配置
    for version, modules in versions_and_modules:
        for module_size in module_sizes:
            qr_pixel_size = modules * module_size
            # 只保留合理大小范围的配置 (150px - 500px)
            if 150 <= qr_pixel_size <= 500:
                qr_configs.append((version, modules, module_size))

    print(f"有效配置数量: {len(qr_configs)}")

    # 按照可能性排序 - 优先测试接近分析结果的配置
    def config_priority(config):
        version, modules, module_size = config
        # 基于分析结果，11px模块大小的权重最高
        size_diff = abs(module_size - 11)
        # 中等版本的权重较高
        version_diff = abs(version - 5)
        return size_diff + version_diff * 0.1

    qr_configs.sort(key=config_priority)

    for i, (version, modules, module_size) in enumerate(qr_configs):
        qr_size = modules * module_size
        print(
            f"\n尝试配置 {i + 1}/{len(qr_configs)}: 版本{version}, {modules}x{modules}模块, 模块大小{module_size}px, 总大小{qr_size}x{qr_size}px")

        # 扩展更多起始位置可能性
        possible_starts = []

        # 1. 基本对齐位置
        possible_starts.extend([
            (0, 0),  # 左上角对齐
            ((400 - qr_size) // 2, (400 - qr_size) // 2),  # 居中对齐
        ])

        # 2. 如果QR码小于图像，尝试更多位置
        if qr_size < 400:
            step = min(20, (400 - qr_size) // 4)  # 步长
            for offset in range(0, 400 - qr_size + 1, step):
                # 沿边界的位置
                possible_starts.extend([
                    (offset, 0),  # 上边界
                    (0, offset),  # 左边界
                    (400 - qr_size, offset),  # 右边界
                    (offset, 400 - qr_size),  # 下边界
                ])

        # 3. 微调位置 (基于中心位置的小幅偏移)
        if qr_size <= 400:
            center_x, center_y = (400 - qr_size) // 2, (400 - qr_size) // 2
            for dx in [-10, -5, 0, 5, 10]:
                for dy in [-10, -5, 0, 5, 10]:
                    new_x, new_y = center_x + dx, center_y + dy
                    if 0 <= new_x <= 400 - qr_size and 0 <= new_y <= 400 - qr_size:
                        possible_starts.append((new_x, new_y))

        # 去重
        possible_starts = list(set(possible_starts))

        for start_x, start_y in possible_starts:
            if start_x < 0 or start_y < 0:
                continue

            if start_x + qr_size > 400 or start_y + qr_size > 400:
                continue

            print(f"  测试起始位置: ({start_x}, {start_y})")

            # 创建修复后的QR码
            # 添加静默区
            quiet_zone = module_size * 4  # 4个模块的静默区
            canvas_size = qr_size + 2 * quiet_zone
            canvas = np.full((canvas_size, canvas_size), 255, dtype=np.uint8)

            # 复制原始数据区域
            end_x = min(start_x + qr_size, 400)
            end_y = min(start_y + qr_size, 400)

            src_region = binary[start_y:end_y, start_x:end_x]
            dst_h, dst_w = src_region.shape

            canvas[quiet_zone:quiet_zone + dst_h, quiet_zone:quiet_zone + dst_w] = src_region

            # 绘制三个定位点
            draw_finder_patterns_precise(canvas, module_size, quiet_zone, modules)

            # 多种解码尝试
            decode_success = False
            result = None

            # 1. 直接解码
            try:
                barcodes = pyzbar.decode(canvas)
                if barcodes:
                    result = barcodes[0].data.decode('utf-8')
                    decode_success = True
            except Exception:
                pass

            # 2. 如果直接解码失败，尝试图像增强
            if not decode_success:
                try:
                    # 形态学操作增强
                    kernel = np.ones((2, 2), np.uint8)
                    enhanced = cv2.morphologyEx(canvas, cv2.MORPH_CLOSE, kernel)
                    enhanced = cv2.morphologyEx(enhanced, cv2.MORPH_OPEN, kernel)

                    barcodes = pyzbar.decode(enhanced)
                    if barcodes:
                        result = barcodes[0].data.decode('utf-8')
                        decode_success = True
                        canvas = enhanced  # 使用增强后的图像
                except Exception:
                    pass

            # 3. 尝试不同的二值化阈值
            if not decode_success:
                for thresh in [100, 150, 180, 200]:
                    try:
                        gray_canvas = canvas.copy()
                        _, thresh_canvas = cv2.threshold(gray_canvas, thresh, 255, cv2.THRESH_BINARY)

                        barcodes = pyzbar.decode(thresh_canvas)
                        if barcodes:
                            result = barcodes[0].data.decode('utf-8')
                            decode_success = True
                            canvas = thresh_canvas
                            break
                    except Exception:
                        continue

            if decode_success:
                print(f"    🎉 成功解码: {result}")

                # 保存成功的修复图像
                base_name = os.path.splitext(image_path)[0]
                success_path = f"{base_name}_final_success.png"
                cv2.imwrite(success_path, canvas)
                print(f"    成功图像已保存: {success_path}")

                return result
            else:
                if i < 5:  # 只显示前5个失败的详细信息
                    print(f"    无法解码")

    print("\n❌ 所有配置都无法成功")
    return None


def draw_finder_patterns_precise(canvas, module_size, offset, modules):
    """绘制精确的定位点"""
    # 定位点的中心位置（距离边缘3.5个模块）
    center_offset = int(3.5 * module_size)

    # 三个定位点的位置
    positions = [
        (offset + center_offset, offset + center_offset),  # 左上
        (offset + modules * module_size - center_offset, offset + center_offset),  # 右上
        (offset + center_offset, offset + modules * module_size - center_offset),  # 左下
    ]

    for center_x, center_y in positions:
        # 绘制7x7模块的定位点
        draw_single_finder_pattern(canvas, center_x, center_y, module_size)


def draw_single_finder_pattern(img, center_x, center_y, module_size):
    """绘制单个定位点 (7x7模块)"""
    # 7x7模块的总大小
    total_size = module_size * 7
    half_size = total_size // 2

    # 计算边界
    x1, y1 = center_x - half_size, center_y - half_size
    x2, y2 = center_x + half_size, center_y + half_size

    # 确保在画布范围内
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(img.shape[1], x2), min(img.shape[0], y2)

    if x2 <= x1 or y2 <= y1:
        return

    # 外层黑色 (7x7)
    cv2.rectangle(img, (x1, y1), (x2, y2), 0, -1)

    # 中间白色 (5x5)
    margin1 = module_size
    inner_x1, inner_y1 = x1 + margin1, y1 + margin1
    inner_x2, inner_y2 = x2 - margin1, y2 - margin1
    if inner_x2 > inner_x1 and inner_y2 > inner_y1:
        cv2.rectangle(img, (inner_x1, inner_y1), (inner_x2, inner_y2), 255, -1)

        # 内层黑色 (3x3)
        margin2 = module_size * 2
        core_x1, core_y1 = x1 + margin2, y1 + margin2
        core_x2, core_y2 = x2 - margin2, y2 - margin2
        if core_x2 > core_x1 and core_y2 > core_y1:
            cv2.rectangle(img, (core_x1, core_y1), (core_x2, core_y2), 0, -1)


def main():
    import sys

    # 支持命令行参数或默认文件
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        image_path = "图片.png"

    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        print("用法: python qr_repair_final.py <图像路径>")
        return

    print("=== 增强版二维码修复工具 ===")
    print(f"处理图像: {image_path}")

    result = create_precise_qr_repair(image_path)

    if result:
        print(f"\n🎉🎉🎉 最终识别结果: {result}")
        print("\n修复成功！")
    else:
        print(f"\n❌ 修复失败")
        print("建议:")
        print("1. 检查图像质量和对比度")
        print("2. 确保二维码占据图像的主要部分")
        print("3. 尝试不同格式或分辨率的图像")


if __name__ == "__main__":
    main()