from scrapy import cmdline

# 执行项目
# scrapy crawl douban_spider -o movielist.json
# 支持 'json', 'jsonlines', 'jl', 'csv', 'xml', 'marshal', 'pickle'
cmdline.execute('scrapy crawl  douban_spider'.split())
