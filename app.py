from flask import Flask, render_template, request, redirect, url_for
from colorthief import ColorThief
import openai
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ✅ 画像から主な色を取得
def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color  # (R, G, B)

# ✅ ChatGPTで紹介文を生成
def generate_character_intro(filename):
    prompt = f"このキャラクター画像のファイル名「{filename}」から想像して、性格・雰囲気・世界観を200文字以内で紹介してください。"
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=200
    )
    return response.choices[0].message["content"]

# ✅ トップページ（アップロード画面）
@app.route('/')
def index():
    return render_template('index.html')

# ✅ アップロード処理＋ユニークURLにリダイレクト
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "ファイルが送信されていません", 400

    file = request.files['file']
    if file.filename == '':
        return "ファイル名が空です", 400

    ext = os.path.splitext(file.filename)[1]
    unique_filename = secure_filename(str(uuid.uuid4()) + ext)

    filepath = os.path.join('static/uploads', unique_filename)
    file.save(filepath)

    # 結果ページへリダイレクト（ユニークURLでアクセス）
    return redirect(url_for('result', filename=unique_filename))

# ✅ 結果ページ（ユニークURL）
@app.route('/result/<filename>')
def result(filename):
    filepath = os.path.join('static/uploads', filename)
    bg_color = get_dominant_color(filepath)
    intro_text = generate_character_intro(filename)

    return render_template(
        'result.html',
        filename=filename,
        bg_color=bg_color,
        intro_text=intro_text
    )

# ✅ Render対応：ポート指定
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
