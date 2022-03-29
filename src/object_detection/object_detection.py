import os
import json
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

import streamlit as st


class ImageRecognition(object):
    def __init__(self, dpth_image=''):
        # クライアントを認証
        with open('./data/secret.json') as f:
            secret = json.load(f)

        KEY = secret['KEY']
        ENDPOINT = secret['ENDPOINT']

        self.computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

        self.dpth_image = dpth_image

    def get_tags(self, fname_image):
        fpth_image = os.path.join(self.dpth_image, fname_image)
        local_image = open(fpth_image, 'rb')
        tags_result = self.computervision_client.tag_image_in_stream(local_image)
        return [tag.name for tag in tags_result.tags]

    def detect_objects(self, fname_image):
        fpth_image = os.path.join(self.dpth_image, fname_image)
        local_image = open(fpth_image, 'rb')
        detect_objects_result = self.computervision_client.detect_objects_in_stream(local_image)
        objects = detect_objects_result.objects
        return objects

def main():
    # アップロードされた画像を保存するディレクトリを作成
    dpth_root = os.path.split(__file__)[0]
    dpth_temp = os.path.join(dpth_root, "temp")
    if not os.path.exists(dpth_temp):
        os.mkdir(dpth_temp)

    st.title('物体検出アプリ')
    uploaded_img = st.file_uploader('Choose an image...', type=['jpg', 'png'])
    if uploaded_img is not None:
        # Azure　の ComputerVisionAPI は画像へのパスを引数とする
        # st.file_uploader は絶対パスを取得できないので
        # 一度作業用ディレクトリに保存して，保存された画像を読み込む
        img = Image.open(uploaded_img)
        fpth_temp = os.path.join(dpth_temp, uploaded_img.name)
        img.save(fpth_temp)

        # 画像処理
        image_recog = ImageRecognition()
        tags = image_recog.get_tags(fpth_temp)
        objects = image_recog.detect_objects(fpth_temp)

        # 出力
        draw = ImageDraw.Draw(img)
        for obj in objects:
            # 矩形の描画
            x = obj.rectangle.x
            y = obj.rectangle.y
            w = obj.rectangle.w
            h = obj.rectangle.h
            draw.rectangle([(x, y), (x + w, y + h)], fill=None, outline='green', width=5)

            # クラス名の描画
            caption = obj.object_property
            font = ImageFont.truetype('./data/Helvetica.ttc', size=20)
            text_w, text_h = draw.textsize(caption, font=font)
            draw.rectangle([(x, y), (x + text_w, y + text_h)], fill='green')
            draw.text((x, y), caption, fill='white', font=font)
        st.image(img)

        st.markdown('**認識されたコンテンツタグ**')
        output_tags = ', '.join(tags)
        st.markdown(f'> {output_tags}')

        # 保存したファイルを削除
        os.remove(fpth_temp)



if __name__ == '__main__':
    main()