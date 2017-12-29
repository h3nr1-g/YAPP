function format() {
    var element = document.getElementById("bodyID");
    if(element != null){
        element.style.backgroundColor = bg_color;
    }

    element = document.getElementById("title");
    if(element != null){
        element.style.color = title_color;
    }

}

function liveMode() {
        window.setInterval(function(){
            location.reload(true);
        }, duration * 1000);
}