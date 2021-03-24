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
    toggle_timeout = setTimeout(function(){ habit_update(id, year, month); }, 2000);
}

function habit_update(id, y, m) {
    var hc = document.getElementById("habit-container_"+id);
    hc.classList.add("inactive");
    socket.emit('habit_changed', {month: [y, m], habit_id: id});
}

socket.on('habit_rendered', function(data) {
    var hc = document.getElementById("habit-container_"+data["habit_id"]);
    var div = document.createElement("div");
    div.innerHTML = data["HTML"];
    hc.parentNode.replaceChild(div.firstChild, hc);
});

function next(year, month) {
    var habit_grid = document.getElementById("habit-grid");
    habit_grid.classList.remove("swipe-in-left");
    habit_grid.classList.remove("swipe-in-right");
    habit_grid.classList.add("swipe-out-left");
    
    socket.emit(
        'month_changed', 
        {
            month: [year, month],
            direction: "forwards"
        }
        );
}

function previous(year, month) {
    var habit_grid = document.getElementById("habit-grid");
    habit_grid.classList.remove("swipe-in-left");
    habit_grid.classList.remove("swipe-in-right");
    habit_grid.classList.add("swipe-out-right");
    
    socket.emit(
        'month_changed', 
        {
            month: [year, month],
            direction: "backwards"
        }
        );
}

socket.on('month_rendered', function(data) {
    clearTimeout(toggle_timeout);
    var habit_grid = document.getElementById("habit-grid");
    habit_grid.innerHTML = data["habits"]["HTML"];
    habit_grid.classList.remove("swipe-out-left");
    habit_grid.classList.remove("swipe-out-right");
    if (data["direction"]=="forwards"){
        habit_grid.classList.add("swipe-in-right");
    } else {
        habit_grid.classList.add("swipe-in-left");
    }
    var month = document.getElementById("month");
    month.innerHTML = data["month"]["HTML"];
});
