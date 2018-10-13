# -*- coding: utf-8 -*-
"""
create on 2018-10-11 下午9:13

author @heyao
"""
import numpy as np
from PIL import Image

from baidu_index import project_path

_templates_sample = [
    ('01.png', [
        ((8, 0, 16, 14), '2', 2), ((16, 0, 24, 14), '1', 1), ((32, 0, 40, 14), '4', 4), ((80, 0, 88, 14), ',', 10),
        ((88, 0, 96, 14), '9', 9), ((128, 0, 136, 14), '3', 3)
    ]),
    ('02.png', [
        ((48, 0, 56, 14), '7', 7), ((152, 0, 160, 14), '0', 0)
    ]),
    ('03.png', [
        ((24, 0, 32, 14), '6', 6), ((56, 0, 64, 14), '5', 5), ((128, 0, 136, 14), '8', 8)
    ])
]


def _make_template(templates):
    image_pipeline = []
    for filename, positions in templates:
        with Image.open('imgs/' + filename) as img:
            for box, num, index in positions:
                image_pipeline.append((img.crop(box), num, index))
    image_pipeline = sorted(image_pipeline, key=lambda x: x[2])
    target_img = Image.new("1", (8 * 11, 14))
    for i, (img, _, _) in enumerate(image_pipeline):
        target_img.paste(img, (i * 8, 0, (i + 1) * 8, 14))
    target_img.save('imgs/template.png')
    target_img.close()


class BaseRecognizer(object):
    def __init__(self, templates_path):
        self.templates_path = templates_path

    def load_templates(self):
        return NotImplementedError("you must implement this function")

    def recognize(self, img):
        return NotImplementedError("you must implement this function")


class BaiduIndexRecognizer(BaseRecognizer):
    """百度指数返回的图片识别"""

    def __init__(self, templates_path, labels='0123456789,', width=6, height=12):
        super(BaiduIndexRecognizer, self).__init__(templates_path)
        self.templates_list = []
        self.labels = labels
        self.width = width
        self.height = height
        self.load_templates()

    def load_templates(self):
        with Image.open(self.templates_path) as templates:
            for i in range(templates.width / self.width):
                box = (i * self.width, 0, (i + 1) * self.width, self.height)
                im = templates.crop(box)
                self.templates_list.append(np.array(im))

    def recognize(self, img):
        """识别函数
        根据每张图片和模板的相似度，选择相似度最高的标签
        :param img: `PIL.Image`
        :return: 
        """
        max_sim = 0
        best_label = ""

        def similarity(arr1, arr2):
            return np.sum(arr1 * arr2) * 1. / (np.linalg.norm(arr1, 2) * np.linalg.norm(arr2, 2))

        img_data = np.array(img)
        for label, im_data in zip(self.labels, self.templates_list):
            sim = similarity(img_data, im_data)
            if sim > max_sim:
                max_sim = sim
                best_label = label
        return best_label


baidu_index_recognizer = BaiduIndexRecognizer(project_path + '/baidu_index/core/imgs/template.png', width=8, height=14)


def recognize_baidu_index(img):
    """识别百度指数图片"""
    for i in range(int(img.size[0] / 8)):
        box = (i * 8, 0, (i + 1) * 8, 14)
        im = img.crop(box)
        yield baidu_index_recognizer.recognize(im)
        im.close()


if __name__ == '__main__':
    _make_template(_templates_sample)
    baidu_index_recognizer = BaiduIndexRecognizer('imgs/template.png', width=8, height=14)
    with Image.open('imgs/01.png') as img:
        print baidu_index_recognizer.recognize(img.crop((32, 0, 40, 14)))
    with Image.open('imgs/template.png') as img:
        print ''.join(list(recognize_baidu_index(img)))
