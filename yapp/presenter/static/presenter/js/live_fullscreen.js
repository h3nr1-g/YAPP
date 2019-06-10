var interval = null;
var seconds_per_picture = 3;
var random_picture_url = "";


function ws_on_receive_callback(data) {
    if (data.mimeType.includes("image/")) {
        show_picture(data.url);
        setTimeout(
            function () {
                if (interval == null) {
                    init_ajax_update(seconds_per_picture, random_picture_url);
                }
            },
            seconds_per_picture * 1000
        );
    } else {
        show_video(data.url, data.mimeType);
    }
    if (data.title != null) {
        //title_tag.innerHTML = data.title + " (Likes: "+String(data.likes)+", Dislikes: "+String(data.dislikes)+")";
        title_tag.innerHTML = data.title + " (Likes: " + String(data.likes) + ")";
    }
    else {
        title_tag.innerHTML = "";
    }
}


function show_picture(url) {
    var video_tag = document.getElementsByTagName("video")[0];
    video_tag.style.width = "0";
    video_tag.style.height = "0";
    video_tag.style["min-height"] = "0%";
    video_tag.style["min-width"] = "0%";
    video_tag.style["max-width"] = "0%";

    var body_tag = document.getElementById("body");
    body_tag.style.backgroundImage = "url('" + url + "')";
}


function show_video(url, mime_type) {
    var video_tag = document.getElementsByTagName("video")[0];
    video_tag.style.height = "100%";
    video_tag.style["min-height"] = "100%";
    video_tag.style["min-width"] = "100%";
    video_tag.style["max-width"] = "100%";
    console.log(video_tag.style);
    video_tag.onended = function () {
        init_ajax_update(seconds_per_picture, random_picture_url);
    };

    var source_tag = document.getElementById("video_source");
    source_tag.setAttribute("src", url);
    source_tag.type = mime_type;

    var body_tag = document.getElementById("body");
    body_tag.style.backgroundImage = "";

    clearInterval(interval);
    interval = null;
    video_tag.load();
    video_tag.play();
}


function ajax_update(xhttp) {
    var data = JSON.parse(xhttp.responseText);
    if (data.mimeType.includes("image/")) {
        show_picture(data.url);
    } else {
        show_video(data.url, data.mimeType);
    }


    var title_tag = document.getElementById("title");
    if (data.title != null) {
        title_tag.innerHTML = data.title + " (Likes: " + String(data.likes) + ", Dislikes: " + String(data.dislikes) + ")";
    }
    else {
        title_tag.innerHTML = "";
    }
}


function init_ajax_update(interval_duration, url) {
    seconds_per_picture = interval_duration;
    random_picture_url = url;

    if (interval == null) {
        interval = setInterval(
            function () {
                ajax_get(url, ajax_update, ajax_fail);
            },
            interval_duration * 1000
        );
    }
}