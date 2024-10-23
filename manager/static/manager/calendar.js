const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'), {
  focus: true
});
const taskDetailsModal = new bootstrap.Modal(document.getElementById('taskDetailsModal'), {
  focus: true
});
var deleteButton = document.getElementById('deleteButton');

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
    eventSources: [
      {
        id: 420,
        url: '/api/events/',
        color: '#6767fe',
        editable: true,
        lazyFetching: true,
      },
      {
        url: '/api/tasks/?exclude=DONE',
        color: '#FF00FF',
        lazyFetching: true,
      }
    ],
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
      var deleteButtonClone = deleteButton.cloneNode(true);
      deleteButton.parentNode.replaceChild(deleteButtonClone, deleteButton);
      deleteButton = deleteButtonClone;
      deleteButton.addEventListener('click', async () => {
        await fetch('/api/events/'.concat(eventObj.id).concat('/'), {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
          }
        });
        calendar.getEventSourceById(420).refetch();
      });
    },
    eventDrop: (eventDropInfo) => {
      updateEventTime(eventDropInfo);
    },
    eventResize: (eventResizeInfo) => {
      updateEventTime(eventResizeInfo);
    },
  });
  calendar.render();
});

async function updateEventTime(eventInfo) {
  var eventObj = eventInfo.event;
  await fetch('/api/events/'.concat(eventObj.id).concat('/'), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    body: JSON.stringify({
      'title': eventObj.title,
      'start_date': eventObj.start.toISOString(),
      'end_date': eventObj.end.toISOString()
    })
  });
}