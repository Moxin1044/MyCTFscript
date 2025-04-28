import argparse
import random

def generate_problem():
    """生成有效的鸡兔同笼问题"""
    while True:
        total = random.randint(10, 100)
        max_legs = 4*total
        legs = random.randint(2*total + 2, max_legs - 2)
        if (legs - 2*total) % 2 == 0:
            return total, legs

def solve_problem(heads, legs):
    """解鸡兔同笼问题"""
    rabbit = (legs - 2 * heads) / 2
    chicken = heads - rabbit
    
    if rabbit < 0 or chicken < 0 or rabbit%1 !=0:
        return None
    return int(chicken), int(rabbit)

def interactive_mode():
    """交互式解题模式"""
    print("模式选择：")
    print("1. 生成题目\n2. 解题\n3. 退出")
    
    while True:
        choice = input("请输入选项：").strip()
        if choice == '1':
            h, f = generate_problem()
            print(f"鸡兔同笼，共有{h}个头，{f}只脚，问鸡兔各几何？")
        elif choice == '2':
            try:
                h = int(input("输入总头数："))
                f = int(input("输入总脚数："))
                result = solve_problem(h, f)
                print(f"解：鸡{result[0]}只，兔{result[1]}只" if result else "无解")
            except ValueError:
                print("输入必须为整数")
        elif choice == '3':
            break
        else:
            print("无效选项")

def batch_solve(file_path):
    """批量解题模式"""
    # 实现文件读取逻辑
    print(f"批量处理文件：{file_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='鸡兔同笼问题生成与求解')
    parser.add_argument('-g', '--generate', type=int, help='生成指定数量的题目')
    parser.add_argument('-s', '--solve', nargs=2, type=int, help='解给定的头脚数')
    parser.add_argument('-f', '--file', help='批量解题文件路径')
    
    args = parser.parse_args()
    
    if args.generate:
        for _ in range(args.generate):
            h, f = generate_problem()
            print(f"头数:{h} 脚数:{f}")
    elif args.solve:
        res = solve_problem(*args.solve)
        print(f"解：{res}" if res else "无解")
    elif args.file:
        batch_solve(args.file)
    else:
        interactive_mode()