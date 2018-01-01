function format() {
    var element = document.getElementById("bodyID");
    if (element !== null) {
        element.style.backgroundColor = bg_color;
    }

    element = document.getElementById("title");
    if (element !== null) {
        element.style.color = title_color;
    }

}

function liveMode() {
    timer = window.setInterval(function () {
        location.reload(true);
    }, duration * 1000);
}


function update_picture(event) {
    document.getElementById("title").innerHTML = "NEW PICTURE "+String(event.data.payload.number);
    document.getElementById("pictureImg").src = event.data.payload.url;
    timer.stop();
    timer.start();
}