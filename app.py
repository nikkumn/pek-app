from flask import Flask, render_template, request
from colorthief import ColorThief
import os

app = Flask(__name__)

# 画像から一番目立つ色を取得する関数
def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color  # (R, G, B)

# ホームページ（アップロードフォーム）表示
@app.route('/')
def index():
    return render_template('index.html')

# 画像アップロード処理と色抽出
@app.route('/upload', methods=['POST'])
def upload():
    # ファイルが送られているかチェック
    if 'file' not in request.files:
        return "ファイルが送信されていません", 400

    file = request.files['file']

    if file.filename == '':
        return "ファイル名が空です", 400

    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)

    # 画像から色を抽出
    bg_color = get_dominant_color(filepath)

    # 結果ページに色とファイル名を渡す
    return render_template('result.html', filename=file.filename, bg_color=bg_color)

# Render用ポート指定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
