var text = 'Meet Attendance CollectorEasy, smart and automatic attendance collection in meet video calls.';
var app_name = document.getElementById('name');
var app_desc = document.getElementById('desc');
var speed = 20000;

function write(i) {

    if (i < 25) {
        app_name.innerHTML += text.charAt(i);
        i++;
        setTimeout(write(i), speed);
    }
    
    else if (i < text.length) {
        app_desc.innerHTML += text.charAt(i);
        i++;
        setTimeout(write(i), speed);
    }

    else {
        i = 0;
        app_name.innerHTML = "";
        app_desc.innerHTML = "";
        setTimeout(write(i), speed);
    }
}

window.addEventListener('load', function () {
    write(0);
})