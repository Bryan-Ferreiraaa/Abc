let imagemBase64 = null;
let imgElemento = new Image();

document.getElementById('image-input').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        imagemBase64 = event.target.result;
        imgElemento.src = imagemBase64;

        imgElemento.onload = function() {
            // Mostrar botões de download
            document.getElementById('btn-jpg').style.display = 'inline-block';
            document.getElementById('btn-png').style.display = 'inline-block';

            // ATIVAR PREVIEW (Resolve o problema de não aparecer)
            document.getElementById('panorama-container').innerHTML = ''; // Limpa antes
            pannellum.viewer('panorama-container', {
                "type": "equirectangular",
                "panorama": imagemBase64,
                "autoLoad": true
            });
        };
    };
    reader.readAsDataURL(file);
});

function baixar(formato) {
    if (!imagemBase64) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // A META: Proporção 2:1 (4096x2048) para o Facebook entender que é 360
    canvas.width = 4096;
    canvas.height = 2048;

    // Preenche fundo e desenha
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(imgElemento, 0, 0, canvas.width, canvas.height);

    const mime = formato === 'png' ? 'image/png' : 'image/jpeg';
    
    // Gera o blob e faz o download
    canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `PANO_360_BRYAN.${formato}`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }, mime, 0.95);
}
