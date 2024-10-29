const eventModalElement = document.getElementById('eventDetailsModal');
const eventDetailsModal = new bootstrap.Modal(
  document.getElementById('eventDetailsModal'),
  {
    focus: true,
  }
);
const taskDetailsModal = new bootstrap.Modal(
  document.getElementById('taskDetailsModal'),
  {
    focus: true,
  }
);
const addEventModal = new bootstrap.Modal(
  document.getElementById('addEventModal'),
  {
    focus: true,
  }
);
const newTitle = document.getElementById('newTitle');
const newStart = document.getElementById('newStart');
const newEnd = document.getElementById('newEnd');
const newDetails = document.getElementById('newDetails');
const addButton = document.getElementById('addButton');
const eventModalTitle = document.getElementById('eventDetailsModalTitle');
const eventTitle = document.getElementById('eventTitle');
const eventStart = document.getElementById('eventStart');
const eventEnd = document.getElementById('eventEnd');
const eventDetails = document.getElementById('eventDetails');
const editButton = document.getElementById('editButton');
const cancelButton = document.getElementById('cancelButton');
let doneButton = document.getElementById('doneButton');
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
        },
      },
    },
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'addEvent dayGridMonth,timeGridWeek,timeGridDay,listWeek',
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
      },
    ],
    eventClick: (eventClickInfo) => {
      const eventObj = eventClickInfo.event;
      const popover = document.querySelector('.fc-popover');
      if (popover !== null) {
        popover.style.display = 'none';
      }

      if (eventObj.extendedProps.type === 'event') {
        updateEventModalInfo(eventObj);
        eventDetailsModal.show();
      } else if (eventObj.extendedProps.type === 'task') {
        const taskDue = formatLocalISO(eventObj.start);
        document.getElementById('taskDetailsModalTitle').innerHTML =
          eventObj.title;
        document.getElementById('taskDue').value = taskDue;
        document.getElementById('taskDetails').value =
          eventObj.extendedProps.details;
        taskDetailsModal.show();
      }

      const deleteButtonClone = deleteButton.cloneNode(true);
      deleteButton.parentNode.replaceChild(deleteButtonClone, deleteButton);
      deleteButton = deleteButtonClone;
      deleteButton.addEventListener('click', async () => {
        await fetch(`/api/events/${eventObj.id}/`, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'),
          },
        });
        calendar.getEventSourceById(420).refetch();
        eventDetailsModal.hide();
      });

      const doneButtonClone = doneButton.cloneNode(true);
      doneButton.parentNode.replaceChild(doneButtonClone, doneButton);
      doneButton = doneButtonClone;
      doneButton.addEventListener('click', async () => {
        const startDate = new Date(eventStart.value);
        const endDate = new Date(eventEnd.value);
        await fetch(`/api/events/${eventObj.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'),
          },
          body: JSON.stringify({
            'title': eventTitle.value,
            'start': startDate.toISOString(),
            'end': endDate.toISOString(),
            'details': eventDetails.value,
          }),
        });
        calendar.getEventSourceById(420).refetch();
        toggleEventInput(false);
      });

      cancelButton.addEventListener('click', () => {
        updateEventModalInfo(eventObj);
        toggleEventInput(false);
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
    },
  });

  addButton.addEventListener('click', async () => {
    const startDate = new Date(newStart.value);
    const endDate = new Date(newEnd.value);
    const userID = JSON.parse(document.getElementById('user_id').textContent);
    await fetch('/api/events/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        'title': newTitle.value,
        'start': startDate.toISOString(),
        'end': endDate.toISOString(),
        'details': newDetails.value,
        'user': userID,
      }),
    });
    newTitle.value = '';
    newStart.value = '';
    newEnd.value = '';
    newDetails.value = '';
    calendar.getEventSourceById(420).refetch();
  });

  editButton.addEventListener('click', () => {
    toggleEventInput(true);
  });

  eventModalElement.addEventListener('hide.bs.modal', () => {
    toggleEventInput(false);
  });

  calendar.render();
});

async function updateEventTime(eventInfo) {
  let eventObj = eventInfo.event;
  await fetch(`/api/events/${eventObj.id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken'),
    },
    body: JSON.stringify({
      'title': eventObj.title,
      'start': eventObj.start.toISOString(),
      'end': eventObj.end.toISOString(),
    }),
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

function updateEventModalInfo(eventObj) {
  const eventStartLocal = formatLocalISO(eventObj.start);
  const eventEndLocal = formatLocalISO(eventObj.end);
  eventModalTitle.innerHTML = eventObj.title;
  eventTitle.value = eventObj.title;
  eventStart.value = eventStartLocal;
  eventEnd.value = eventEndLocal;
  eventDetails.value = eventObj.extendedProps.details;
}

function toggleEventInput(on) {
  if (on) {
    editButton.classList.add('hidden');
    deleteButton.classList.add('hidden');
    doneButton.classList.remove('hidden');
    cancelButton.classList.remove('hidden');
    eventTitle.parentNode.classList.remove('hidden');
    eventStart.removeAttribute('readonly');
    eventStart.setAttribute('class', 'form-control');
    eventEnd.removeAttribute('readonly');
    eventEnd.setAttribute('class', 'form-control');
    eventDetails.removeAttribute('readonly');
    eventDetails.setAttribute('class', 'form-control');
  } else {
    editButton.classList.remove('hidden');
    deleteButton.classList.remove('hidden');
    doneButton.classList.add('hidden');
    cancelButton.classList.add('hidden');
    eventTitle.parentNode.classList.add('hidden');
    eventStart.setAttribute('readonly', true);
    eventStart.setAttribute('class', 'form-control-plaintext');
    eventEnd.setAttribute('readonly', true);
    eventEnd.setAttribute('class', 'form-control-plaintext');
    eventDetails.setAttribute('readonly', true);
    eventDetails.setAttribute('class', 'form-control-plaintext');
  }
}
