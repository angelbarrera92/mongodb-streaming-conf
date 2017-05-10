$(document).ready(function() {

    var logTable = $('#logTable').DataTable({
        "order": [[ 0, "desc" ]]
    });

    var socket = io.connect('http://' + document.domain + ':' + location.port);
    socket.on('connect', function() {
        socket.emit('connected', {
            data: 'I\'m connected!'
        });
    });
    socket.on('log', function(data) {
        logTable.row.add([
            data.time.$date,
            data.host,
            data.name,
            data.levelname,
            data.msg
        ]).draw(false);
        logTable.columns.adjust().draw();
    });

});
