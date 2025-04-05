from flask import Flask, render_template, request
from colorthief import ColorThief
import os

app = Flask(__name__)

# ステップ 2・3：画像から一番目立つ色を取得する関数
def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color  # (R, G, B) の形式で返す

# ステップ 4：アップロードされた画像を保存して色を取得
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file.filename != '':
        filepath = os.path.join('static/uploads', file.filename)
        file.save(filepath)

        # 画像から背景色を抽出！
        bg_color = get_dominant_color(filepath)

        # HTMLに画像と背景色を渡す
        return render_template('result.html', filename=file.filename, bg_color=bg_color)

# ホームページ表示用（アップロードフォーム）
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "ファイルが送信されていません（'file' が見つかりません）", 400

    file = request.files['file']
    if file.filename == '':
        return "ファイル名が空です", 400

    filepath = os.path.join('static/uploads', file.filename)
    file.save(filepath)

    bg_color = get_dominant_color(filepath)
    return render_template('result.html', filename=file.filename, bg_color=bg_color)

# Render用のポート設定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
