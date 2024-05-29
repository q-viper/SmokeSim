// Get color picker element
const colorPicker = document.getElementById('color-picker');
// Get color display element
const colorDisplay = document.getElementById('color-display');

// Get sliders
const maxLife = document.getElementById('maxLife');
const minLife = document.getElementById('minLife');
const maxNumParticles = document.getElementById('maxNumParticles');
const MaxNumParticlesDisplay = document.getElementById('selectedMaxNumParticles');
const MaxLifeDisplay = document.getElementById('selectedMaxLife');
const MinLifeDisplay = document.getElementById('selectedMinLife');
const clearSmokeBtn = document.getElementById('clearSmoke-btn');
const opacity = document.getElementById('opacity');
const opacityDisplay = document.getElementById('selectedOpacity');
var maxVx = document.getElementById('maxVx');
var minVx = document.getElementById('minVx');
var maxVy = document.getElementById('maxVy');
var minVy = document.getElementById('minVy');
var maxScale = document.getElementById('maxScale');
var minScale = document.getElementById('minScale');
var spriteSize = document.getElementById('spriteSize');
var maxVxDisplay = document.getElementById('maxVxDisplay');
var minVxDisplay = document.getElementById('minVxDisplay');
var maxVyDisplay = document.getElementById('maxVyDisplay');
var minVyDisplay = document.getElementById('minVyDisplay');
var maxScaleDisplay = document.getElementById('maxScaleDisplay');
var minScaleDisplay = document.getElementById('minScaleDisplay');
var spriteSizeDisplay = document.getElementById('spriteSizeDisplay');


var blendAlpha = 1.0;
var isClearSmoke = false;
var divider = 100;




// Function to convert HEX color to RGBA
function getColorRGBA(hex) {
    // Remove '#' from the beginning of the string
    hex = hex.substring(1);
    // Parse hex string to an integer
    const bigint = parseInt(hex, 16);
    // Extract red, green, and blue values
    var r = (bigint >> 16) & 255;
    var g = (bigint >> 8) & 255;
    var b = bigint & 255;
    // r, g, b into floating point values
    r *= 1.0;
    g *= 1.0;
    b *= 1.0;

    // Return RGBA value
    return [r, g, b];
}
function smokeCanvas(canvas, blendedCanvas) {
    MaxLifeDisplay.innerHTML = `MaxLife: ${maxLife.value}`;
    MinLifeDisplay.innerHTML = `minLife: ${minLife.value}`;
    MaxNumParticlesDisplay.innerHTML = `MaxParticles: ${maxNumParticles.value}`;
    minVyDisplay.innerHTML = `MinVy: ${minVy.value}`;
    minVxDisplay.innerHTML = `MinVx: ${minVx.value}`;
    maxScaleDisplay.innerHTML = `MaxScale: ${maxScale.value}`;
    maxVxDisplay.innerHTML = `MaxVx: ${maxVx.value}`;
    maxVyDisplay.innerHTML = `MaxVy: ${maxVy.value}`;
    minScaleDisplay.innerHTML = `MinScale: ${minScale.value}`;
    spriteSizeDisplay.innerHTML = `SpriteSize: ${spriteSize.value}`;
    opacityDisplay.innerHTML = `Opacity: ${opacity.value}`;
    // Get RGBA value of the selected color
    const rgbaValue = getColorRGBA(colorPicker.value);
    // Display RGBA value
    colorDisplay.textContent = `RGBA: ${rgbaValue}`;

    ctx = canvas.getContext('2d');
    var maxLifeValue = maxLife.value;
    var numParticles = maxNumParticles.value;

    var currentScreenWidth = window.innerWidth;
    var currentScreenHeight = window.innerHeight;

    // find relative position of cursor


    // canvas.width = innerWidth;
    // canvas.height = innerHeight;
    // console.log(canvas.width, canvas.height);
    var color = getColorRGBA(colorPicker.value);
    console.log((maxScale.value + minScale.value) / 2);
    var party = smokemachine([ctx], color, spriteSize.value);
    party.start(); // start animating
    var n = numParticles;
    var t = Math.floor(Math.random() * maxLife.value * 200);
    // create dictionary for lifetime
    var options = {
        lifetime: t,
        minVx: minVx.value / 1.0,
        maxVx: maxVx.value / 1.0,
        minVy: minVy.value / 1.0,
        maxVy: maxVy.value / 1.0,
        minScale: minScale.value / 1.0,
        maxScale: maxScale.value / 1.0,
        minLifetime: minLife.value / 1.0,
        maxLifetime: t + 1,
    }

    console.log(options);
    party.setPreDrawCallback(function (dt) {
        party.addSmoke(canvas.width / 2, canvas.height, numParticles, options);
        canvas.width = innerWidth;
        canvas.height = innerHeight;
    });

    onclick = e => {

        const mouseX = e.clientX;
        const mouseY = e.clientY;

        const areaRect = blendedCanvas.getBoundingClientRect();
        const areaLeft = areaRect.left;
        const areaTop = areaRect.top;
        const areaRight = areaRect.right;
        const areaBottom = areaRect.bottom;

        const clearButtonRect = clearSmokeBtn.getBoundingClientRect();
        const clearButtonLeft = clearButtonRect.left;
        const clearButtonTop = clearButtonRect.top;
        const clearButtonRight = clearButtonRect.right;
        const clearButtonBottom = clearButtonRect.bottom;

        console.log("MouseX: " + mouseX + " MouseY: " + mouseY + " IW " + innerWidth + " IH " + innerHeight);
        // console.log(areaLeft, areaTop, areaRight, areaBottom);
        console.log("AreaLeft: " + areaLeft + " AreaTop: " + areaTop + " AreaRight: " + areaRight + " AreaBottom: " + areaBottom);

        // Check if the mouse is within the defined area
        if (mouseX >= areaLeft && mouseX <= areaRight && mouseY >= areaTop && mouseY <= areaBottom) {
            // var x = mouseX - areaLeft;
            // var y = mouseY - areaTop;
            var dx = (areaRight - areaLeft);
            var dy = (areaBottom - areaTop);
            var x = innerWidth * (mouseX - areaLeft) / dx;
            var y = innerHeight * (mouseY - areaTop) / dy;

            // Change cursor style if mouse is within the area
            document.body.style.cursor = 'pointer'; // Change cursor to pointer
            console.log('NewXY', x, y);


            var n = numParticles;
            var t = Math.floor(Math.random() * maxLife);
            var options = {
                lifetime: t,
                minVx: minVx.value / 1.0,
                maxVx: maxVx.value / 1.0,
                minVy: minVy.value / 1.0,
                maxVy: maxVy.value / 1.0,
                minScale: minScale.value / 1.0,
                maxScale: maxScale.value / 1.0,
                minLifetime: 0,
                maxLifetime: t + 1,
            }

            party.setPreDrawCallback(function (dt) {
                party.addSmoke(x, y, n, options);
                canvas.width = innerWidth;
                canvas.height = innerHeight;
            });
        }
        else if (mouseX >= clearButtonLeft && mouseX <= clearButtonRight && mouseY >= clearButtonTop && mouseY <= clearButtonBottom) {
            // Change cursor style if mouse is within the area
            document.body.style.cursor = 'pointer'; // Change cursor to pointer
            console.log('Clear Smoke');
            party.updateAndDrawParticles(1000);
            party.setPreDrawCallback(function (dt) {
                // party.step(1);
                party.addSmoke(0, 0, 0.5, 0.5);
            });

        }
        else {
            // Reset cursor style if mouse is outside the area
            document.body.style.cursor = 'default'; // Reset cursor to default
            console.log('Not Hoveringnnnnn');
        }
    };

    onmousemove = function (e) {

        const mouseX = e.clientX;
        const mouseY = e.clientY;

        const areaRect = blendedCanvas.getBoundingClientRect();
        const areaLeft = areaRect.left;
        const areaTop = areaRect.top;
        const areaRight = areaRect.right;
        const areaBottom = areaRect.bottom;

        // Check if the mouse is within the defined area
        if (mouseX >= areaLeft && mouseX <= areaRight && mouseY >= areaTop && mouseY <= areaBottom) {
            var dx = (areaRight - areaLeft);
            var dy = (areaBottom - areaTop);
            var x = innerWidth * (mouseX - areaLeft) / dx;
            var y = innerHeight * (mouseY - areaTop) / dy;

            // Change cursor style if mouse is within the area
            document.body.style.cursor = 'pointer'; // Change cursor to pointer
            console.log('Hovering', x, y);
            var n = numParticles;
            var t = Math.floor(Math.random() * maxLife) / 100;
            var options = {
                lifetime: t,
                minVx: minVx.value / 1.0,
                maxVx: maxVx.value / 1.0,
                minVy: minVy.value / 1.0,
                maxVy: maxVy.value / 1.0,
                minScale: minScale.value / 1.0,
                maxScale: maxScale.value / 1.0,
                minLifetime: 0,
                maxLifetime: t + 1,
            }
            party.addSmoke(x, y, n, options);
        } else {
            // Reset cursor style if mouse is outside the area
            document.body.style.cursor = 'default'; // Reset cursor to default
            console.log('Not Hoveringnnnnn');
        }
    };
    return party;
}
var canvas = document.getElementById('smoke-canvas');
var blendedCanvas = document.getElementById('blended-canvas');

var smokeParty = smokeCanvas(canvas, blendedCanvas);

maxLife.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);
});
maxNumParticles.addEventListener('input', function () {

    smokeParty = smokeCanvas(canvas, blendedCanvas);
});
maxVx.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);
});
minVx.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);

});
maxVy.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);
});
minVy.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);

});
maxScale.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);

});
minScale.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);

});
spriteSize.addEventListener('input', function () {
    smokeParty = smokeCanvas(canvas, blendedCanvas);

});


// Event listener for color picker input change
colorPicker.addEventListener('input', function () {

    smokeParty = smokeCanvas(canvas, blendedCanvas);
});
// event listener for clearSmoke button
clearSmokeBtn.addEventListener('click', function () {
    isClearSmoke = true;
    // smokeParty = smokeCanvas(canvas, blendedCanvas);


});
opacity.addEventListener('input', function () {
    blendAlpha = opacity.value / 100;
});