var socket = io();
socket.on('connect', function() {
    var d = new Date();
    socket.emit(
        'user_connected', 
        {user_date: [d.getFullYear(), d.getMonth()+1, d.getDate()]}
        );
});