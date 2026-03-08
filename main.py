from flask import Flask, request, send_file, render_template_string
from PIL import Image
import io
import os

app = Flask(__name__)

# O "CÓDIGO SECRETO" XMP que o Facebook procura
XMP_TAG = (
    '<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="Adobe XMP Core 5.1.0-jc003">'
    '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
    '<rdf:Description rdf:about="" xmlns:GPano="http://ns.google.com/photos/1.0/panorama/">'
    '<GPano:ProjectionType>equirectangular</GPano:ProjectionType>'
    '<GPano:UsePanoramaViewer>True</GPano:UsePanoramaViewer>'
    '<GPano:FullPanoWidthPixels>4096</GPano:FullPanoWidthPixels>'
    '<GPano:FullPanoHeightPixels>2048</GPano:FullPanoHeightPixels>'
    '<GPano:CroppedAreaImageWidthPixels>4096</GPano:CroppedAreaImageWidthPixels>'
    '<GPano:CroppedAreaImageHeightPixels>2048</GPano:CroppedAreaImageHeightPixels>'
    '<GPano:CroppedAreaLeftPixels>0</GPano:CroppedAreaLeftPixels>'
    '<GPano:CroppedAreaTopPixels>0</GPano:CroppedAreaTopPixels>'
    '</rdf:Description></rdf:RDF></x:xmpmeta>'
)

@app.route('/')
def index():
    return '''
        <h1>Conversor 360 Profissional</h1>
        <form action="/convert" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <button type="submit">Converter para 360° Real</button>
        </form>
    '''

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['image']
    img = Image.open(file.stream)
    
    # 1. Força a proporção 2:1 (4096x2048)
    img = img.convert("RGB")
    img_360 = img.resize((4096, 2048), Image.Resampling.LANCZOS)
    
    # 2. Salva em um buffer na memória
    img_io = io.BytesIO()
    # Injeta o XMP nos metadados do JPEG (isso o JS não faz direito)
    img_360.save(img_io, 'JPEG', quality=90, xmp=XMP_TAG)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='FOTO_360_REAL.jpg')

if __name__ == '__main__':
    app.run(debug=True)
