import requests
import argparse
from tabulate import tabulate

def search_github_repositories(query, token, sort='stars', order='desc', per_page=10):
    url = 'https://api.github.com/search/repositories'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Python-API-Request'
    }
    params = {
        'q': query,
        'sort': sort,
        'order': order,
        'per_page': per_page
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"API错误: {response.status_code} - {response.text}")
        return None
    
    data = response.json()
    return data['items']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GitHub仓库搜索工具')
    parser.add_argument('--query', required=False, help='搜索关键词')
    parser.add_argument('--token', required=False, help='GitHub访问令牌')
    parser.add_argument('--sort', default='stars', choices=['stars', 'forks', 'updated'], help='排序方式（默认: stars）')
    parser.add_argument('--order', default='desc', choices=['asc', 'desc'], help='排序顺序（默认: desc）')
    parser.add_argument('--per_page', type=int, default=10, help='每页结果数量（默认: 10）')
    
    args = parser.parse_args()

    # 交互式输入缺失参数
    if not args.query:
        args.query = input('请输入搜索关键词：')
    if not args.token:
        args.token = input('请输入GitHub访问令牌：')
    
    results = search_github_repositories(
        query=args.query,
        token=args.token,
        sort=args.sort,
        order=args.order,
        per_page=args.per_page
    )
    
    if results:
        table_data = []
        headers = ['仓库名称', 'URL', '描述', '星数', '最后更新']
        
        for repo in results:
            table_data.append([
                repo['name'],
                repo['html_url'],
                repo['description'] or '无描述',
                repo['stargazers_count'],
                repo['updated_at']
            ])
        
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print(f"\n找到 {len(results)} 个匹配的仓库")
    else:
        print("没有找到匹配的仓库或发生错误")
