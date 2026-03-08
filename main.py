from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

# Metadados XMP que "ativam" o giro 360 no Facebook/Google
XMP_TAG = (
    '<?xpacket begin="" id="W5M0MpCehiHzreSzNTczkc9d"?>'
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
    '<?xpacket end="r"?>'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'image' not in request.files:
        return "Nenhuma imagem enviada", 400
    
    file = request.files['image']
    img = Image.open(file.stream)
    
    # Converte para RGB (evita erro com PNG transparente)
    img = img.convert("RGB")
    
    # Redimensiona para 4096x2048 (Proporção de Ouro 2:1)
    img_360 = img.resize((4096, 2048), Image.Resampling.LANCZOS)
    
    img_io = io.BytesIO()
    # SALVA INJETANDO O XMP (O segredo que o JavaScript não consegue fazer)
    img_360.save(img_io, 'JPEG', quality=90, xmp=XMP_TAG)
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/jpeg', as_attachment=True, download_name='PANO_360_REAL.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
