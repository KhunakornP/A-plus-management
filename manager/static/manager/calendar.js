const allEvents = JSON.parse(document.getElementById('events-data').textContent);
const allTasks = JSON.parse(document.getElementById('tasks-data').textContent);
const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'), {
  focus: true
});
const taskDetailsModal = new bootstrap.Modal(document.getElementById('taskDetailsModal'), {
  focus: true
});

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
    height: '90vh',
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
        document.getElementById('eventDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('eventStart').value = eventObj.start.toISOString().slice(0, 16);
        document.getElementById('eventEnd').value = eventObj.end.toISOString().slice(0, 16);
        document.getElementById('eventDetails').value = eventObj.extendedProps.details;
        eventDetailsModal.show();
      } else if (eventObj.extendedProps.type == "task") {
        document.getElementById('taskDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('taskDue').value = eventObj.start.toISOString().slice(0, 16);
        document.getElementById('taskDetails').value = eventObj.extendedProps.details;
        taskDetailsModal.show();
      }
    },
    eventDrop: (eventDropInfo) => {
      var eventObj = eventDropInfo.event;
      fetch(eventObj.extendedProps.update, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: JSON.stringify({
          'title': eventObj.title,
          'start_date': eventObj.start.toISOString().slice(0, 16),
          'end_date': eventObj.end.toISOString().slice(0, 16)
        })
      });
    },
    eventResize: (eventResizeInfo) => {
      var eventObj = eventResizeInfo.event;
      fetch(eventObj.extendedProps.update, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: JSON.stringify({
          'title': eventObj.title,
          'start_date': eventObj.start.toISOString().slice(0, 16),
          'end_date': eventObj.end.toISOString().slice(0, 16)
        })
      })
    }
  });
  calendar.render();
});