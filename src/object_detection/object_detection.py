from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from charset_normalizer import detect
from msrest.authentication import CognitiveServicesCredentials

import os
import json

class ImageRecognition(object):
    def __init__(self, dpth_image):
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
    dpth_image = './data'
    image_recog = ImageRecognition(dpth_image)
    tags = image_recog.get_tags('objects.jpg')
    print(tags)
    objects = image_recog.detect_objects('objects.jpg')
    print(objects)

if __name__ == '__main__':
    main()