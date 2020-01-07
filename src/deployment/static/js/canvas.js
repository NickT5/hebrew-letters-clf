window.addEventListener('load', () => {
    const canvas = document.querySelector('#canvas');
    const ctx = canvas.getContext('2d');

    const btnClear = document.querySelector('#btnClear');

    let isDrawing = false;

    function resizeCanvas(w, h){
        //canvas.width = window.innerWidth;
        //canvas.height = window.innerHeight;
        canvas.width = w;
        canvas.height = h;
    }

    function start(event){
        isDrawing = true;
        draw(event);
    }

    function stop(){
        isDrawing = false;
        ctx.beginPath();
    }

    function draw({clientX: mx, clientY: my}){
        if(!isDrawing) return;

        x = mx - canvas.offsetLeft;
        y = my - canvas.offsetTop;

        //if(x <= 0 || x >= canvas.width) isDrawing = false; return;
        //if(y <= 0 || y >= canvas.height) isDrawing = false; return;

        ctx.lineWidth = 3;
        ctx.lineCap = "round";
        ctx.strokeStyle = "#000000";

        ctx.lineTo(x, y);
        ctx.stroke();
        //Makes lines smoother, less pixelated
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function clearCanvas(){
        ctx.clearRect(0,0 , canvas.width, canvas.height);
    }

    //EventListeners
    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stop);
    btnClear.addEventListener('click', clearCanvas);

    resizeCanvas(150, 150);

});
