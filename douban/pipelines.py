# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import jieba


# 处理数据
class DoubanPipeline(object):
    def process_item(self, item, spider):
        self.down_snapshot(item)
        self.save2csv(item)

    # 下载电影图片快照
    def down_snapshot(self, item):
        snapshot_ulr = item['snapshot']
        get = requests.get(snapshot_ulr)
        split = snapshot_ulr.split('.')
        with open('./data/' + item['movie_name'] + "." + split[len(split) - 1], 'wb') as f:
            f.write(get.content)

    # 保存数据到CSV
    def save2csv(self, item):
        df = pd.DataFrame(columns=['comment'], data=item['comments'])
        path = './data/' + item['movie_name'] + '.csv'
        df.to_csv(path, encoding='utf-8')
        comments_ = item['comments']
        jieba_comments = jieba.lcut(str(comments_))
        comments = " ".join(jieba_comments)
        print(comments)
        img = Image.open('ciyun2.png')
        img_array = np.array(img)
        wc = WordCloud(width=900, height=900, background_color='white', font_path='simhei.ttf', mask=img_array,
                       stopwords=STOPWORDS, contour_width=1, contour_color='steelblue')
        wc.generate(comments)
        wc.to_file('temp1.png')


if '__main__' == __name__:
    df = pd.read_csv('./data/temp1.csv')
    comment_list = df['comment'].values.tolist()
    jieba_comments = jieba.lcut(str(comment_list))
    comments = " ".join(jieba_comments)
    print(comments)
    img = Image.open('ciyun2.png')
    img_array = np.array(img)
    wc = WordCloud(width=2000, height=1800, background_color='white', font_path='simhei.ttf', mask=img_array,
                   stopwords=STOPWORDS, contour_width=3, contour_color='steelblue')
    wc.generate(comments)
    wc.to_file('temp1.png')
    pass
