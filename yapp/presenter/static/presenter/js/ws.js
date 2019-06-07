function init_ws(ws_url,receive_callback_function) {
    var connection = new WebSocket(ws_url, ['soap', 'xmpp']);

    connection.onopen = function () {
    };

// Log errors
    connection.onerror = function (error) {
        console.log('WebSocket Error: ' + error);
    };

// Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server sent: ' + e.data);
        var data = JSON.parse(e.data);

        receive_callback_function(data)
    }
}