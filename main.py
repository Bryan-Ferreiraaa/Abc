from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

# O "Carimbo" 360 que faz a mágica
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

@app.route('/convert/<format_type>', methods=['POST'])
def convert(format_type):
    file = request.files['image']
    img = Image.open(file.stream).convert("RGB")
    
    # Redimensionamento de alta qualidade 2:1
    img_360 = img.resize((4096, 2048), Image.Resampling.LANCZOS)
    img_io = io.BytesIO()

    if format_type == 'png':
        # PNG Full (Pesado)
        img_360.save(img_io, 'PNG', xmp=XMP_TAG)
        name = "PANO_360_FULL.png"
        mime = "image/png"
    else:
        # JPG Leve (Photooxy style)
        img_360.save(img_io, 'JPEG', quality=85, xmp=XMP_TAG)
        name = "PANO_360_LEVE.jpg"
        mime = "image/jpeg"

    img_io.seek(0)
    return send_file(img_io, mimetype=mime, as_attachment=True, download_name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
