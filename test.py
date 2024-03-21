import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 定义博客网站的链接和 RSS 文件名
blog_url = 'https://blog.sciencenet.cn/blog.php'
rss_file = 'feed.xml'

# 下载网页内容
response = requests.get(blog_url)
html_content = response.content

# 解析网页内容
soup = BeautifulSoup(html_content, 'html.parser')
articles = soup.find_all('article')

# 格式化 RSS 内容
rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
  <channel>
    <title>Example Blog</title>
    <link>{blog_url}</link>
    <description>Latest articles from Example Blog</description>
"""

for article in articles:
    title = article.find('h2').text.strip()
    link = article.find('a')['href']
    pub_date = article.find('time')['datetime']
    pub_date = datetime.strptime(pub_date, '%Y-%m-%d').strftime('%a, %d %b %Y %H:%M:%S %z')

    rss_content += f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <pubDate>{pub_date}</pubDate>
    </item>
"""

rss_content += """
  </channel>
</rss>
"""

# 保存为 XML 文件
with open(rss_file, 'w') as file:
    file.write(rss_content)

print(f"RSS 文件已生成：{rss_file}")
