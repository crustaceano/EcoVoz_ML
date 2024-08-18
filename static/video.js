document.addEventListener('DOMContentLoaded', () => {
    const videoStream = document.getElementById('video-stream');
    const startButton = document.getElementById('start-camera');
    const stopButton = document.getElementById('stop-camera');

    startButton.addEventListener('click', () => {
        fetch('/start_camera', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                videoStream.src = '/video_feed';
            })
            .catch(error => console.error('Error starting camera:', error));
    });

    stopButton.addEventListener('click', () => {
        fetch('/stop_camera', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log(data.message);
                videoStream.src = '';
            })
            .catch(error => console.error('Error stopping camera:', error));
    });

    videoStream.onerror = () => {
        videoStream.src = '';
        console.error('Error in video stream');
    };
});
