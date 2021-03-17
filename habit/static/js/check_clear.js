function toggle(dom_element) {
    id = dom_element.getAttribute("data-calendar-id")
    day = dom_element.getAttribute("data-day")
    socket.emit(
        'date_toggled', 
        {
            day: day,
            calendar_id: id,
        }
        );
}

