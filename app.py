from flask import Flask
from cnstd import CnStd
from cnocr import CnOcr
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

def base64_to_pil(base64_str):
    image = base64.b64decode(base64_str)
    image = BytesIO(image)
    image = Image.open(image)
    return image


@app.route('/ocr', method="POST")
def ocr_process():
    data = flask.get_data()
    image_b64 = data["image"]
    image_pil = base64_to_pil(image_b64)

    box_infos = cn_std.detect(image_pil)

    for box_info in box_infos['detected_texts']:
        cropped_img = box_info['cropped_img']
        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        print('ocr result: %s' % str(ocr_res))


if __name__ == '__main__':
    cn_std = CnStd()
    cn_ocr = CnOcr()

    app.run()
