const allEvents = JSON.parse(document.getElementById('events-data').textContent)

document.addEventListener('DOMContentLoaded', function() {
  var calendarElement = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarElement, {
    themeSystem: 'bootstrap5',
    initialView: 'dayGridMonth',
    nowIndicator: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    navLinks: true,
    editable: true,
    selectable: true,
    selectMirror: true,
    dayMaxEvents: true,
    timeZone: 'UTC',
    events: allEvents
  });
  calendar.render();
})