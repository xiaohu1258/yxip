import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime

# 目标URL列表
urls = [
    'https://api.uouin.com/cloudflare.html',
    'https://ip.164746.xyz'
]

# 正则：匹配IP
ip_pattern = r'\b\d{1,3}(?:\.\d{1,3}){3}\b'
ip_set = set()  # 用于去重

for url in urls:
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        if url in ['https://api.uouin.com/cloudflare.html', 'https://ip.164746.xyz']:
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')

        for element in elements:
            text = element.get_text()
            ip_matches = re.findall(ip_pattern, text)
            ip_set.update(ip_matches)

    except Exception as e:
        print(f"⚠ 请求或解析失败: {url} - {e}")

# 排序，写入文件
sorted_ips = sorted(ip_set)

with open('ip.txt', 'w', encoding='utf-8') as f:
    for ip in sorted_ips:
        f.write(ip + '\n')


print(f"✅ 收集到 {len(sorted_ips)} 个 IP，已写入 ip.txt")
