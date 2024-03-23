var video = document.getElementById('video');
var canvas = document.getElementById('smoke-canvas');
var ctx = canvas.getContext('2d');
var blendedCanvas = document.getElementById('blended-canvas');
var blendedCtx = blendedCanvas.getContext('2d');
var tempCanvas = document.createElement('canvas');
var tempCtx = tempCanvas.getContext('2d');
var sourceURL = video.querySelector('source').src;
var videoSource = document.getElementById('video-url');


const changeVideo = document.getElementById('changeVid-btn');
changeVideo.addEventListener('click', function () {
    const newSource = videoSource.value;
    if (newSource) {
        video.querySelector('source').src = newSource;
        video.load();
    }
});

// When video is playing, draw the current frame to the canvas
video.addEventListener('play', function () {
    var $this = this; // Cache video element
    (function loop() {
        if (!$this.paused && !$this.ended) {

            tempCanvas.width = innerWidth; // video.width;
            tempCanvas.height = innerHeight; // video.height;
            tempCtx.drawImage($this, 0, 0, innerWidth, innerHeight);
            requestAnimationFrame(loop);

        }
    })();
});


// Download all images when button is clicked
document.getElementById("download-btn").addEventListener("click", function () {
    var link1 = document.createElement('a');
    var fname = sourceURL.split('/').pop().split('.')[0] + '_ts_' + video.currentTime;
    link1.download = 'smoke_' + fname + '.png';
    link1.href = canvas.toDataURL();
    link1.click();

    var link2 = document.createElement('a');
    link2.download = 'blended_' + fname + '.png';
    link2.href = blendedCanvas.toDataURL();
    link2.click();

    var link3 = document.createElement('a');
    link3.download = fname + '.png';
    link3.href = tempCanvas.toDataURL();
    link3.click();
});