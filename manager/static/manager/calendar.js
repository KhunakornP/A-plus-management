const eventDetailsModal = new bootstrap.Modal('#eventDetailsModal');
const taskDetailsModal = new bootstrap.Modal('#taskDetailsModal');
const addEventModal = new bootstrap.Modal('#addEventModal');
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
const deleteButton = document.getElementById('deleteButton');
let currentEventID = 0;
let calendar;

import { formatLocalISO, getErrorDiv, insertErrorDiv, removeErrorDivs } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  const calendarElement = document.getElementById('calendar');
  calendar = new FullCalendar.Calendar(calendarElement, {
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
      currentEventID = eventObj.id;
      if (popover !== null) {
        popover.style.display = 'none';
      }

      if (eventObj.extendedProps.type === 'event') {
        loadEventModalInfo(eventObj);
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

      cancelButton.addEventListener('click', () => {
        removeErrorDivs();
        eventTitle.classList.remove('is-invalid');
        loadEventModalInfo(eventObj);
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
    const errorMessages = [];
    const startDate = new Date(newStart.value);
    const endDate = new Date(newEnd.value);
    const userID = JSON.parse(document.getElementById('user_id').textContent);
    removeErrorDivs();
    newTitle.classList.remove('is-invalid');
    newStart.classList.remove('is-invalid');
    newEnd.classList.remove('is-invalid');
    try {
      if (newTitle.value === '') {
        errorMessages.push({name: 'Title', message: 'Event title cannot be blanked.'})
      }
      if (newStart.value === '') {
        errorMessages.push({name: 'Start', message: 'Event start date cannot be blanked.'})
      }
      if (newEnd.value === '') {
        errorMessages.push({name: 'End', message: 'Event end date cannot be blanked.'})
      }
      if (endDate < startDate) {
        errorMessages.push({name: 'Date', message: 'Event end date must be after start date.'})
      }
      if (errorMessages.length > 0) {
        throw new Error();
      }
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
      addEventModal.hide();
    } catch (error) {
      errorMessages.forEach((e) => {
        if (e.name === 'Title') {
          newTitle.classList.add('is-invalid');
          const errorTitleText = getErrorDiv(e.message, 'error-title-add');
          insertErrorDiv(newTitle, errorTitleText);
        }
        if (e.name === 'Start') {
          newStart.classList.add('is-invalid');
          const errorStartText = getErrorDiv(e.message, 'error-start-add');
          insertErrorDiv(newStart, errorStartText)
        }
        if (e.name === 'End') {
          newEnd.classList.add('is-invalid');
          const errorEndText = getErrorDiv(e.message, 'error-end-add');
          insertErrorDiv(newEnd, errorEndText);
        }
        if (e.name === 'Date') {
          newEnd.classList.add('is-invalid');
          const errorDateText = getErrorDiv(e.message, 'error-date-add');
          insertErrorDiv(newEnd, errorDateText);
        }
      })
    }
  });

  editButton.addEventListener('click', () => {
    if (editButton.innerText === 'Edit') {
      toggleEventInput(true);
    } else {
      updateEvent();
    }
  });

  document.getElementById('eventDetailsModal').addEventListener('hide.bs.modal', () => {
    toggleEventInput(false);
    eventTitle.classList.remove('is-invalid');
    removeErrorDivs();
  });

  document.getElementById('addEventModal').addEventListener('hide.bs.modal', () => {
    newTitle.classList.remove('is-invalid');
    newStart.classList.remove('is-invalid');
    newEnd.classList.remove('is-invalid');
    removeErrorDivs();
  });

  deleteButton.addEventListener('click', async () => {
    await fetch(`/api/events/${currentEventID}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
    });
    calendar.getEventSourceById(420).refetch();
    eventDetailsModal.hide();
  });

  calendar.render();
});

async function updateEvent() {
  const errorMessages = [];
  const startDate = new Date(eventStart.value);
  const endDate = new Date(eventEnd.value);
  removeErrorDivs();
  eventTitle.classList.remove('is-invalid');
  eventStart.classList.remove('is-invalid');
  eventEnd.classList.remove('is-invalid');
  try {
    if (eventTitle.value === '') {
      errorMessages.push({name: 'Title', message: 'Event title cannot be blanked.'})
    }
    if (eventStart.value === '') {
      errorMessages.push({name: 'Start', message: 'Event start date cannot be blanked.'})
    }
    if (eventEnd.value === '') {
      errorMessages.push({name: 'End', message: 'Event end date cannot be blanked.'})
    }
    if (endDate < startDate) {
      errorMessages.push({name: 'Date', message: 'Event end date must be after start date.'})
    }
    if (errorMessages.length > 0) {
      throw new Error();
    }
    await fetch(`/api/events/${currentEventID}/`, {
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
    })
    calendar.getEventSourceById(420).refetch();
    eventModalTitle.innerHTML = eventTitle.value;
    toggleEventInput(false);
  } catch (error) {
    errorMessages.forEach((e) => {
      if (e.name === 'Title') {
        eventTitle.classList.add('is-invalid');
        const errorTitleText = getErrorDiv(e.message, 'error-title-update');
        insertErrorDiv(eventTitle, errorTitleText);
      }
      if (e.name === 'Start') {
        eventStart.classList.add('is-invalid');
        const errorStartText = getErrorDiv(e.message, 'error-start-update');
        insertErrorDiv(eventStart, errorStartText)
      }
      if (e.name === 'End') {
        eventEnd.classList.add('is-invalid');
        const errorEndText = getErrorDiv(e.message, 'error-end-update');
        insertErrorDiv(eventEnd, errorEndText);
      }
      if (e.name === 'Date') {
        eventEnd.classList.add('is-invalid');
        const errorDateText = getErrorDiv(e.message, 'error-date-update');
        insertErrorDiv(eventEnd, errorDateText);
      }
    })
  }
}

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

function loadEventModalInfo(eventObj) {
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
    editButton.innerHTML = 'Done';
    deleteButton.classList.add('hidden');
    cancelButton.classList.remove('hidden');
    eventTitle.parentNode.classList.remove('hidden');
    eventStart.removeAttribute('readonly');
    eventStart.setAttribute('class', 'form-control');
    eventEnd.removeAttribute('readonly');
    eventEnd.setAttribute('class', 'form-control');
    eventDetails.removeAttribute('readonly');
    eventDetails.setAttribute('class', 'form-control');
  } else {
    editButton.innerHTML = 'Edit';
    deleteButton.classList.remove('hidden');
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
