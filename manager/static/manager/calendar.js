const eventDetailsModal = new bootstrap.Modal(document.getElementById('eventDetailsModal'), {
  focus: true
});
const taskDetailsModal = new bootstrap.Modal(document.getElementById('taskDetailsModal'), {
  focus: true
});
const addEventModal = new bootstrap.Modal(document.getElementById('addEventModal'), {
  focus: true
});
const newTitle = document.getElementById('newTitle');
const newStart = document.getElementById('newStart');
const newEnd = document.getElementById('newEnd');
const newDetails = document.getElementById('newDetails');
const addButton = document.getElementById('addButton');
let deleteButton = document.getElementById('deleteButton');

document.addEventListener('DOMContentLoaded', () => {
  const calendarElement = document.getElementById('calendar');
  let calendar = new FullCalendar.Calendar(calendarElement, {
    initialView: 'dayGridMonth',
    nowIndicator: true,
    allDaySlot: false,
    customButtons: {
      addEvent: {
        text: 'Add Event',
        click: () => {
          addEventModal.show();
        }
      },
    },
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'addEvent dayGridMonth,timeGridWeek,timeGridDay,listWeek'
    },
    height: '90vh',
    navLinks: true,
    selectable: true,
    dayMaxEvents: true,
    timeZone: 'local',
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
      const eventObj = eventClickInfo.event;
      const popover = document.querySelector('.fc-popover');
      if (popover !== null) {
        popover.style.display = 'none';
      }
      if (eventObj.extendedProps.type == "event") {
        const eventStart = formatLocalISO(eventObj.start);
        const eventEnd = formatLocalISO(eventObj.end);
        console.log(eventObj.start.toISOString());
        document.getElementById('eventDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('eventStart').value = eventStart;
        document.getElementById('eventEnd').value = eventEnd;
        document.getElementById('eventDetails').value = eventObj.extendedProps.details;
        eventDetailsModal.show();
      } else if (eventObj.extendedProps.type == "task") {
        const taskDue = formatLocalISO(eventObj.start);
        document.getElementById('taskDetailsModalTitle').innerHTML = eventObj.title;
        document.getElementById('taskDue').value = taskDue;
        document.getElementById('taskDetails').value = eventObj.extendedProps.details;
        taskDetailsModal.show();
      }
      const deleteButtonClone = deleteButton.cloneNode(true);
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
        eventDetailsModal.hide();
      });
    },
    eventDrop: (eventDropInfo) => {
      updateEventTime(eventDropInfo);
    },
    eventResize: (eventResizeInfo) => {
      updateEventTime(eventResizeInfo);
    },
    select: (selectionInfo) => {
      newStart.value = formatLocalISO(selectionInfo.start);
      newEnd.value = formatLocalISO(selectionInfo.end);
    }
  });

  addButton.addEventListener('click', async () => {
    const startDate = new Date(newStart.value);
    const endDate = new Date(newEnd.value);
    await fetch('/api/events/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: JSON.stringify({
        'title': newTitle.value,
        'start': startDate.toISOString(),
        'end': endDate.toISOString(),
        'details': newDetails.value
      })
    });
    newTitle.value = '';
    newStart.value = '';
    newEnd.value = '';
    newDetails.value = '';
    calendar.getEventSourceById(420).refetch();
  });

  calendar.render();
});

async function updateEventTime(eventInfo) {
  let eventObj = eventInfo.event;
  await fetch('/api/events/'.concat(eventObj.id).concat('/'), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    body: JSON.stringify({
      'title': eventObj.title,
      'start': eventObj.start.toISOString(),
      'end': eventObj.end.toISOString()
    })
  });
}

function formatLocalISO(dateUTC) {
  const dateTime = new Date(dateUTC.toISOString());
  const timeZoneOffSet = dateTime.getTimezoneOffset() * 60 * 1000;
  let dateTimeLocal = dateTime - timeZoneOffSet;
  dateTimeLocal = new Date(dateTimeLocal);
  let iso = dateTimeLocal.toISOString();
  iso = iso.split('.')[0];
  iso = iso.replace('T', ' ');
  return iso;
}
