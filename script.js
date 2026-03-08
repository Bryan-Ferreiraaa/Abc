let imgOriginal = null;

document.getElementById('arquivo').onchange = function(e) {
    const reader = new FileReader();
    reader.onload = function(event) {
        imgOriginal = new Image();
        imgOriginal.onload = function() {
            // Preview para você ver se carregou
            pannellum.viewer('panorama', {
                "type": "equirectangular",
                "panorama": event.target.result,
                "autoLoad": true
            });
        };
        imgOriginal.src = event.target.result;
    };
    reader.readAsDataURL(e.target.files[0]);
};

function converter(formato) {
    if(!imgOriginal) return alert("Escolha uma foto primeiro!");

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    // Proporção obrigatória 2:1
    canvas.width = 4096;
    canvas.height = 2048;
    ctx.drawImage(imgOriginal, 0, 0, canvas.width, canvas.height);

    const mime = formato === 'png' ? 'image/png' : 'image/jpeg';
    
    canvas.toBlob((blob) => {
        // Criar o link de download
        const link = document.createElement('a');
        link.download = `PANO_360_BRYAN.${formato}`;
        link.href = URL.createObjectURL(blob);
        link.click();
    }, mime, 0.9);
}
