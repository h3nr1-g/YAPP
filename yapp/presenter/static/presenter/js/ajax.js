function ajax_get(url, okay_200_function, non_200_function){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        okay_200_function(this);
    }
    if (this.readyState == 4 && this.status != 200) {
        non_200_function(this);
    }

  };
  xhttp.open("GET", url, true);
  xhttp.send();
}

function ajax_delete_and_reload(url){
  if(confirm("Wollen Sie dieses Element wirklich löschen?")){
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            window.location.reload();
        }
      };
      xhttp.open("DELETE", url, true);
      xhttp.send();
  }
}

function ajax_fail(ajax_request) {
    alert("Received response with status code: "+String(ajax_request.status));
}