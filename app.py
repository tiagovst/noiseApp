from io import BytesIO
from PIL import Image
import tempfile
import base64
import numpy as np
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# Diretório onde os uploads de imagens serão salvos
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Rota para lidar com o upload da imagem
@app.route('/upload', methods=['POST'])
def upload():
    # Verificar se o arquivo foi enviado
    if 'imagem' not in request.files:
        return redirect(request.url)

    imagem = request.files['imagem']

    # Verificar se o arquivo tem um nome
    if imagem.filename == '':
        return redirect(request.url)

    # Processar a imagem e adicionar ruído
    intensidade_do_ruido = 0.1  # Ajuste a intensidade do ruído conforme necessário
    imagem_original = Image.open(imagem)
    imagem_original = imagem_original.convert('RGB')
    imagem_array = np.array(imagem_original)
    ruido = np.random.normal(loc=0, scale=intensidade_do_ruido, size=imagem_array.shape).astype(np.uint8)
    imagem_ruidosa = np.clip(imagem_array + ruido, 0, 255)
    imagem_com_ruido = Image.fromarray(imagem_ruidosa)

    # Converter a imagem com ruído para dados base64
    buffered = BytesIO()
    imagem_com_ruido.save(buffered, format="JPEG")
    imagem_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return render_template('result.html', imagem_base64=imagem_base64)


if __name__ == '__main__':
    app.run(debug=False)
