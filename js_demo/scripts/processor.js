let processor = {
    timerCallback: function () {
        // if (this.video.paused || this.video.ended) {
        //     return;
        // }
        this.computeFrame();
        let self = this;
        setTimeout(function () {
            self.timerCallback();
        }, 0);
    },

    doLoad: function () {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('smoke-canvas');
        this.canvasCtx = canvas.getContext('2d');

        this.blendedCanvas = document.getElementById('blended-canvas');
        this.blendedCtx = blendedCanvas.getContext('2d');

        this.video.setAttribute('crossOrigin', 'Anonymous');
        this.canvas.setAttribute('crossOrigin', 'Anonymous');
        this.blendedCanvas.setAttribute('crossOrigin', 'Anonymous');

        let self = this;
        this.video.addEventListener("play", function () {
            self.blendedCanvas.width = innerWidth;
            self.blendedCanvas.height = innerHeight;
            self.width = self.video.width;
            self.height = self.video.height;
            self.timerCallback();
        }, false);
    },

    computeFrame: function () {
        this.blendedCtx.drawImage(this.video, 0, 0, innerWidth, innerHeight);
        this.blendedCtx.globalAlpha = blendAlpha;
        this.blendedCtx.drawImage(canvas, 0, 0, innerWidth, innerHeight);
        this.blendedCtx.globalAlpha = 1.0;

        return;
    }
};

document.addEventListener("DOMContentLoaded", () => {
    processor.doLoad();
});