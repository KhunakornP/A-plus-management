const allEvents = JSON.parse(document.getElementById('events-data').textContent);
const allTasks = JSON.parse(document.getElementById('tasks-data').textContent);

document.addEventListener('DOMContentLoaded', () => {
  var calendarElement = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarElement, {
    initialView: 'dayGridMonth',
    nowIndicator: true,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    navLinks: true,
    selectable: true,
    dayMaxEvents: true,
    timeZone: 'UTC',
    events: allEvents.concat(allTasks),
    eventClick: (eventClickInfo) => {
      var eventObj = eventClickInfo.event;
      var popover = document.querySelector('.fc-popover');
      if (popover !== null) {
        popover.style.display = 'none';
      }
      if (eventObj.extendedProps.type == "event") {
        var detailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'), {
          focus: true
        });
        document.getElementById('eventDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('eventStart').value = eventObj.start.toISOString().slice(0, 16);
        document.getElementById('eventEnd').value = eventObj.end.toISOString().slice(0, 16);
        document.getElementById('eventDetails').value = eventObj.extendedProps.details;
      } else if (eventObj.extendedProps.type == "task") {
        var detailsModal = new bootstrap.Modal(document.getElementById('taskDetailsModal'), {
          focus: true
        });
        document.getElementById('taskDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('taskDue').value = eventObj.start.toISOString().slice(0, 16);
        document.getElementById('taskDetails').value = eventObj.extendedProps.details;
      }
      detailsModal.show()
    },

    eventDrop: (eventDropInfo) => {
      alert('Event dropped to: ' + eventDropInfo.event.start.toUTCString());
    }
  });
  calendar.render();
});