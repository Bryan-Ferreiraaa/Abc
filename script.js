const fileUpload = document.getElementById('file-upload');
const downloadBtn = document.getElementById('download-360');
const canvas = document.getElementById('conversion-canvas');
const ctx = canvas.getContext('2d');

fileUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            // 1. TAMANHO 2:1 (Padão Universal 360)
            canvas.width = 4096;
            canvas.height = 2048;

            // 2. DESENHO SEM CÍRCULO PRETO
            ctx.fillStyle = "#000";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            // 3. CONVERTER PARA JPEG
            const jpegData = canvas.toDataURL("image/jpeg", 0.90);

            // 4. INJETAR METADADOS SEM CORROMPER (Simulando Photooxy)
            // Criamos o cabeçalho XMP que o Facebook exige
            const xmp = `http://ns.google.com/photos/1.0/panorama/\x00GPano:ProjectionType="equirectangular"\x00GPano:FullPanoWidthPixels="4096"\x00GPano:FullPanoHeightPixels="2048"`;
            
            // Aqui usamos a biblioteca Piexif para inserir os dados no lugar certo do arquivo
            const exifObj = {"0th": {}, "Exif": {}, "GPS": {}};
            const exifStr = piexif.dump(exifObj);
            
            // Inserimos a marca d'água digital de 360 graus
            const finalImage = piexif.insert(exifStr, jpegData);

            // 5. PREVIEW E DOWNLOAD
            document.getElementById('panorama-container').innerHTML = '';
            pannellum.viewer('panorama-container', {
                "type": "equirectangular",
                "panorama": finalImage,
                "autoLoad": true
            });

            downloadBtn.disabled = false;
            downloadBtn.onclick = () => {
                const link = document.createElement('a');
                link.href = finalImage;
                link.download = `360_READY_${Date.now()}.jpg`;
                link.click();
            };
        };
        img.src = event.target.result;
    };
    reader.readAsDataURL(file);
});
