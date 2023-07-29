function filelen(){
    const images = document.getElementById("image").files;
    const submit = document.getElementById("submit");
    const message = document.getElementById('message');
    if(images.length <= 2 && 0 < images.length){
        message.innerHTML = "画像を保存しました！";
    }else{
        pass
    }
}
setInterval(filelen, 500);


navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            document.getElementById('video').srcObject = stream;
        });
        // Capture image on canvas when enter key is pressed
        document.addEventListener('keydown', function(e) {
            if (e.key === "Enter") {
                var canvas = document.getElementById('canvas');
                var context = canvas.getContext('2d');
                const message = document.getElementById('message');
                message.innerHTML = "画像を保存しました！";
                // context.drawImage(document.getElementById('video'), 0, 0, 200, 150);
                // Convert canvas to jpeg
                const id = location.pathname.split("/")[1];
                var jpeg = canvas.toDataURL("image/jpeg");
        
                // Send data to server
                fetch('/camera/'+id, {
                    method: 'POST',
                    body: JSON.stringify({ img: jpeg }),
                    headers: { 'Content-Type': 'application/json' }
                })
                .then(response => response.json())
                .then(data => window.location.href = data.redirect);
            }
        });

