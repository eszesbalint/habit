var socket = io();

socket.on('connect', function() {
    var d = new Date();
    socket.emit(
        'user_connected', 
        {user_date: [d.getFullYear(), d.getMonth()+1, d.getDate()]}
        );
});

var toggle_timeout;
function toggle(dom_element) {
    clearTimeout(toggle_timeout);
    id = parseInt(dom_element.getAttribute("data-habit-id"));
    year = parseInt(dom_element.getAttribute("data-year"));
    month = parseInt(dom_element.getAttribute("data-month"));
    day = parseInt(dom_element.getAttribute("data-day"));
    socket.emit(
        'date_toggled', 
        {
            date: [year, month, day],
            habit_id: id,
        }
        );
    toggle_timeout = setTimeout(function(){ request_render(year, month); }, 2000);
}

function request_render(year, month) {
    var habit_grid = document.getElementById("habit-grid");
    habit_grid.classList.add("inactive");
    socket.emit(
        'month_changed', 
        {
            month: [year, month],
        }
        );
}

socket.on('habits_rendered', function(data) {
    var habit_grid = document.getElementById("habit-grid");
    habit_grid.innerHTML = data["HTML"];
    habit_grid.classList.remove("inactive");
});
