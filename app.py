from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files['image']
    if image.filename == '':
        return 'ファイルが選ばれていません'
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    html_content = f'''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
      <meta charset="UTF-8">
      <title>キャラプロフィール</title>
      <style>
        body {{
          background: linear-gradient(to bottom, #ffeaff, #ffffff);
          font-family: 'Rounded Mplus 1c', 'Arial Rounded MT Bold', sans-serif;
          text-align: center;
          padding: 40px;
          color: #444;
        }}
        h1 {{
          font-size: 2rem;
          color: #ff66cc;
        }}
        img {{
          border-radius: 20px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
          max-width: 300px;
          margin-top: 20px;
        }}
        .card {{
          background: #fff;
          border-radius: 16px;
          padding: 20px;
          max-width: 500px;
          margin: 0 auto;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
      </style>
    </head>
    <body>
      <div class="card">
        <h1>あなたのキャラページができました！</h1>
        <img src="/{image_path}" alt="キャラ画像">
        <p>かわいいですね！また会いにきてね♪</p>
      </div>
    </body>
    </html>
    '''

    result_path = os.path.join('templates', 'result.html')
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

