from wordcloud import WordCloud, STOPWORDS
import jieba
import numpy
from PIL import Image
import pandas as pd

if __name__ == '__main__':
    csv = pd.read_csv('./data/12.csv')
    values__tolist = csv['comment'].values.tolist()
    lcut = jieba.lcut(str(values__tolist))
    join = ' '.join(lcut)
    image = Image.open('ciyun2.png')
    image_array = numpy.array(image)
    cloud = WordCloud(font_path='simhei.ttf', width=1200, height=900, contour_width=1, mask=image_array,
                      background_color='white')
    cloud.generate(join)
    # cloud.generate_from_frequencies()
    image = cloud.to_image()
    image.show('')
