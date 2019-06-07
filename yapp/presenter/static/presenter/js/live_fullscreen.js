var interval = null;
var seconds_per_picture = 3;
var random_picture_url = "";


function ws_on_receive_callback(data) {
    clearInterval(interval);
    interval=null;
    var body_tag = document.getElementById("body");
    body_tag.style.backgroundImage = "url('"+data.url+"')";
    var title_tag = document.getElementById("title");
    console.log(data);
    if(data.title != null){
        //title_tag.innerHTML = data.title + " (Likes: "+String(data.likes)+", Dislikes: "+String(data.dislikes)+")";
        title_tag.innerHTML = data.title + " (Likes: "+String(data.likes)+")";
    }
    else {
        title_tag.innerHTML = "";
    }
    setTimeout(
        function () {
             if(interval== null) {
                 init_ajax_update(seconds_per_picture, random_picture_url);
             }
        },
        seconds_per_picture * 1000
    );
}


function ajax_update_picture(xhttp){
    var data = JSON.parse(xhttp.responseText);
    var body_tag = document.getElementById("body");
    body_tag.style.backgroundImage = "url('"+data.url+"')";
    var title_tag = document.getElementById("title");
    if(data.title != null){
        //title_tag.innerHTML = data.title + " (Likes: "+String(data.likes)+", Dislikes: "+String(data.dislikes)+")";
        title_tag.innerHTML = data.title + " (Likes: "+String(data.likes)+")";
    }
    else {
        title_tag.innerHTML = "";
    }
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