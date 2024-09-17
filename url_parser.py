from urllib.parse import urlparse
import pandas as pd
import time
import re

start_time = time.time()

# CSVファイルを読み込む
df = pd.read_csv('output_urls.csv')

domains_df = pd.read_csv('shorturl.csv')
tld_list = pd.read_csv('newgTLD.csv')
domains_list = domains_df['domain'].tolist()

# TLDリストをセットに変換
tld_set = set(tld_list['newgTLD'].tolist())

def count_subdomain(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        return 0
    parts = hostname.split('.')
    if len(parts) <= 2:
        return 0
    return len(parts) - 2

def count_FQDNlength(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        return 0
    return len(hostname)

def include_ip(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        return 0
    
    ipv4_pattern = re.compile(r'(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])')
    match = ipv4_pattern.search(hostname)
    if match:
        return 1
    return 0

def shortning_service(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        return 0
    for domain in domains_list:
        if domain in hostname:
            return 1
    return 0


def contains_specific_words(url):
    specific_words = ['secure', 'account', 'webscr', 'login', 'api', 'signin', 'banking', 'confirm']
    for word in specific_words:
        # 単語境界を考慮した正規表現パターンを作成
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        if pattern.search(url):
            return word
    return None

def count_special_characters(url):
    special_characters = ['@', '?', '%']
    return sum(url.count(char) for char in special_characters)

def protocol_type(url):
    if url.startswith('https'):
        return 'https'
    elif url.startswith('http'):
        return 'http'
    return 'other'

def extract_domain_parts(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    if not hostname:
        return '', '', ''
    
    parts = hostname.split('.')

    if len(parts) >= 4:
        top_level_domain = parts[-1]
        second_level_domain = parts[-2]
        third_level_domain = parts[-3]

    elif len(parts) == 3:
        top_level_domain = parts[-1]
        second_level_domain = parts[-2]
        third_level_domain = parts[-3]

    elif len(parts) == 2:
        top_level_domain = parts[-1]
        second_level_domain = parts[-2]
        third_level_domain = ''
    else:
        top_level_domain = parts[-1]
        second_level_domain = ''
        third_level_domain = ''
    
    
    return top_level_domain.replace('.', ''), second_level_domain.replace('.', ''), third_level_domain.replace('.', '')

def is_newgTLD(top_level_domain):
    return 1 if top_level_domain.replace('.', '') in tld_set else 0

# ドメイン部分を抽出して、それぞれの列に分割して保存
df['top_level_domain'], df['second_level_domain'], df['third_level_domain'] = zip(*df['url'].apply(extract_domain_parts))

# 各機能を適用して新しい列を追加する
df['subdomain_count'] = df['url'].apply(count_subdomain)
df['FQDN_length'] = df['url'].apply(count_FQDNlength)
df['ip_include'] = df['url'].apply(include_ip)
df['shortning_service'] = df['url'].apply(shortning_service)
df['newgTLD'] = df['top_level_domain'].apply(is_newgTLD)
df['contains_specific_words'] = df['url'].apply(contains_specific_words)
df['special_characters_count'] = df['url'].apply(count_special_characters)
df['protocol_type'] = df['url'].apply(protocol_type)

# 新しいCSVファイルに結果を保存する
df.to_csv('aa.csv', index=False)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")
