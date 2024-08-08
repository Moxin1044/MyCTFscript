import requests
import pandas as pd


def check_domain(domain):
    http_status = None
    https_status = None
    print(f"正在检测 {domain}")

    try:
        response = requests.get(f'http://{domain}', timeout=5)
        http_status = response.status_code
    except requests.RequestException:
        http_status = 'Error'

    try:
        response = requests.get(f'https://{domain}', timeout=5)
        https_status = response.status_code
    except requests.RequestException:
        https_status = 'Error'

    return http_status, https_status


def process_domains(domains_file, output_xlsx):
    domains = []
    with open(domains_file, 'r', encoding='utf-8') as file:
        for line in file:
            domain = line.strip()
            if domain:
                http_status, https_status = check_domain(domain)
                domains.append({'Domain': domain, 'HTTP Status': http_status, 'HTTPS Status': https_status})

    df = pd.DataFrame(domains)
    df.to_excel(output_xlsx, index=False, engine='openpyxl')


process_domains('纯域名资产.txt', 'output.xlsx')