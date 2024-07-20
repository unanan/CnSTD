from flask import Flask, request, jsonify
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


def box_jsonify(box):
    output_box = []
    for point in box:
        output_box.append([float(point[0]), float(point[1])])
    return output_box


@app.route('/ocr', methods=["POST"])
def ocr_process():
    image_b64 = request.json.get("image")
    image_pil = base64_to_pil(image_b64)

    box_infos = cn_std.detect(image_pil)

    results = []
    for box_info in box_infos['detected_texts']:
        cropped_img = box_info['cropped_img']
        ocr_res = cn_ocr.ocr_for_single_line(cropped_img)
        results.append({
            "box": box_jsonify(box_info["box"]),
            "text": ocr_res["text"],
            "score": float(ocr_res["score"])
        })
    return jsonify(results)


if __name__ == '__main__':
    cn_std = CnStd()
    cn_ocr = CnOcr()

    app.run(host="0.0.0.0", port=8288)  # 临时占用
