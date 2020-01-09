window.addEventListener('load', () => {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    const btnClear = document.getElementById('btnClear');
    //const btnSubmit = document.getElementById('submit');

    let isDrawing = false;

    function resizeCanvas(w, h){
        //canvas.width = window.innerWidth;
        //canvas.height = window.innerHeight;
        canvas.width = w;
        canvas.height = h;
    }

    function start(event){
        console.log('start')
        isDrawing = true;
        draw(event);
    }

    function stop(){
        console.log('stop')
        isDrawing = false;
        ctx.beginPath();
        setDrawing();
    }

    function draw({clientX: mx, clientY: my}){
        if(!isDrawing) return;

        x = mx - canvas.offsetLeft;
        y = my - canvas.offsetTop;

        //if(x <= 0 || x >= canvas.width) isDrawing = false; return;
        //if(y <= 0 || y >= canvas.height) isDrawing = false; return;

        ctx.lineWidth = 9;
        ctx.lineCap = "round";
        ctx.strokeStyle = "#000000"; //black color

        ctx.lineTo(x, y);
        ctx.stroke();
        //Makes lines smoother, less pixelated
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function clearCanvas(){
        ctx.clearRect(0,0 , canvas.width, canvas.height);
        document.getElementById('data').value = ""
    }

    function setDrawing(){
        //document.getElementById('data').value = canvas.toDataURL('image/jpeg', 1.0);
        document.getElementById('data').value = canvas.toDataURL();
    }

    //EventListeners
    canvas.addEventListener('mousedown', start);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stop);
    btnClear.addEventListener('click', clearCanvas);
    //btnSubmit.addEventListener('click', setDrawing);

    resizeCanvas(150, 150);

});
