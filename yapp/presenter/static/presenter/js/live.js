var interval = null;
var seconds_per_picture = 3;
var random_picture_url = "";


function ws_on_receive_callback(data) {
    clearInterval(interval);
    interval=null;
    var img_tag = document.getElementById("live_picture");
    img_tag.src = data.url;
    setTimeout(
        function () {
             if(interval== null) {
                 init_ajax_update(seconds_per_picture, random_picture_url);
             }
        },
        (seconds_per_picture+2) * 1000
    );
}


function ajax_update_picture(xhttp){
    var data = JSON.parse(xhttp.responseText);
    var img_tag = document.getElementById("live_picture");
    img_tag.src = data.url;
}


function init_ajax_update(interval_duration, url) {
    seconds_per_picture = interval_duration;
    random_picture_url = url;
    if(interval == null){
        interval = setInterval(
            function () {
                ajax_get(url,ajax_update_picture,ajax_fail);
            },
            interval_duration * 1000
        );
    }
}