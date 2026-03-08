const fileUpload = document.getElementById('image-input');
const btnJpg = document.getElementById('btn-jpg');
const btnPng = document.getElementById('btn-png');
const panoramaContainer = document.getElementById('panorama-container');
let imagemOriginal = null;

// 1. Detecta o carregamento da imagem
fileUpload.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(event) {
        imagemOriginal = new Image();
        imagemOriginal.onload = function() {
            // Ativa os botões de download
            btnJpg.style.display = 'inline-block';
            btnPng.style.display = 'inline-block';

            // Inicia o Preview 360 (Pannellum)
            panoramaContainer.innerHTML = '';
            pannellum.viewer('panorama-container', {
                "type": "equirectangular",
                "panorama": event.target.result,
                "autoLoad": true,
                "vaov": 180,
                "haov": 360
            });
        };
        imagemOriginal.src = event.target.result;
    };
    reader.readAsDataURL(file);
});

// 2. Função de Conversão e Download (Executada no Navegador)
function baixar360(formato) {
    if (!imagemOriginal) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Forçamos a Proporção de Ouro 2:1 (4096x2048)
    // Isso é o que "engana" o Facebook para ativar o modo 360
    canvas.width = 4096;
    canvas.height = 2048;

    // Desenha a imagem esticando-a para preencher toda a esfera
    ctx.fillStyle = "#000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(imagemOriginal, 0, 0, canvas.width, canvas.height);

    const mime = formato === 'png' ? 'image/png' : 'image/jpeg';
    const qualidade = formato === 'png' ? 1.0 : 0.9;

    canvas.toBlob((blob) => {
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        
        // Nome do arquivo com prefixo PANO_ para reconhecimento automático
        link.download = `PANO_360_CONVERTIDO.${formato}`;
        
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }, mime, qualidade);
}
