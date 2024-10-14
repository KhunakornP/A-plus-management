document.addEventListener('DOMContentLoaded', function() {
  var calendarElement = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarElement, {
    initialView: 'dayGridMonth'
  });
  calendar.render();
})