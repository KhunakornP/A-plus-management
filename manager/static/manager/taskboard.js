const columns = document.querySelectorAll('.drop_area')
const offcanvas = new bootstrap.Offcanvas('#task-offcanvas')
const createTaskModal = new bootstrap.Modal('#addTask')
const deleteBtn = document.getElementById('del-task-btn')
const editBtn = document.getElementById('edit-task-btn')
const createBtn = document.getElementById('create-task-btn')
const taskOffcanvasTitle = document.getElementById('task-title')
const taskOffcanvasDetails = document.getElementById('task-details');
const taskOffcanvasEndDate = document.getElementById('task-enddate');
const taskOffcanvasET = document.getElementById('task-et');
const taskModalTitle = document.getElementById('modal-task-title');
const taskModalEndDate = document.getElementById('modal-task-enddate');
const taskModalStatus = document.getElementById('modal-task-status');
const taskModalDetails = document.getElementById('modal-task-details')
const taskModalET = document.getElementById('modal-task-et');
const taskboardID = window.location.href.split('/').slice(-2)[0];
let currentTaskID = 0;

async function updateTask(){
  await fetch(`/api/tasks/${currentTaskID}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    body: JSON.stringify({
      'title': taskOffcanvasTitle.value,
      'details': taskOffcanvasDetails.value,
      'end_date': getValidDateISOString(taskOffcanvasEndDate.value),
      'time_estimate': getValidEstimatedTime(taskOffcanvasET.value)
    })
  });
  renderColumns()
}

function toggleOffcanvasFields(on) {
  if(on) {
    taskOffcanvasTitle.removeAttribute('readonly');
    taskOffcanvasTitle.setAttribute('class', 'form-control');
    taskOffcanvasDetails.removeAttribute('readonly');
    taskOffcanvasDetails.setAttribute('class', 'form-control');
    taskOffcanvasEndDate.removeAttribute('readonly');
    taskOffcanvasEndDate.setAttribute('class', 'form-control');
    taskOffcanvasET.removeAttribute('readonly');
    taskOffcanvasET.setAttribute('class', 'form-control');
  }
  else {
    taskOffcanvasTitle.setAttribute('readonly', true);
    taskOffcanvasTitle.setAttribute('class', 'form-control-plaintext');
    taskOffcanvasDetails.setAttribute('readonly', true);
    taskOffcanvasDetails.setAttribute('class', 'form-control-plaintext');
    taskOffcanvasEndDate.setAttribute('readonly', true);
    taskOffcanvasEndDate.setAttribute('class', 'form-control-plaintext');
    taskOffcanvasET.setAttribute('readonly', true);
    taskOffcanvasET.setAttribute('class', 'form-control-plaintext');
  }
}

async function fetchTasksJSON() {
  const response = await fetch(`/api/tasks/?taskboard=${taskboardID}`);
  const tasks = await response.json();
  return tasks;
}

function generateTaskCard(task) {
  const card = document.createElement('div');
  card.classList.add("bg-body", "border", "border-white", "shadow-lg",
    "rounded", "overflow-hidden", "m-3", "draggable", "text-center", "py-2")
  card.setAttribute('draggable', true);

  const innerCard = document.createElement('div')
  innerCard.classList.add("my-0", "py-0", "link-light", "task-card")
  innerCard.innerHTML = `<u>${task.title}</u>`
  innerCard.addEventListener('click', () => {
    offcanvas.show();
    currentTaskID = task.id;
    taskOffcanvasTitle.value = `${task.title}`;
    taskOffcanvasET.value = `${task.time_estimate}`;
    taskOffcanvasEndDate.value = formatLocalISOFromString(task.end_date);
    if (task.details !== null) {
      taskOffcanvasDetails.value = `${task.details}`;
    }
    else {
      taskOffcanvasDetails.value = "";
    }
  })
  card.appendChild(innerCard);
  card.addEventListener('dragstart', () => {
    currentTaskID = task.id;
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', async () => {
    card.classList.remove('dragging');
    await fetch(`/api/tasks/${currentTaskID}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
      },
      body: JSON.stringify({
        'status': card.parentNode.id
      })
    });
  });
  return card
}

async function appendColumnChildren(children, column) {
  if(column !== null) {
    for (const child of children) {
      column.appendChild(generateTaskCard(child));
    }
  }
}

async function renderColumns() {
  for (const column of columns) {
    column.innerHTML = '';
  };
  const response = await fetch(`/api/tasks/?taskboard=${taskboardID}`);
  const tasks = await response.json();
  const toDoTasks = tasks.filter(task => task.status === 'TODO')
  const inProgressTasks = tasks.filter(task => task.status === 'IN PROGRESS')
  const doneTasks = tasks.filter(task => task.status === 'DONE')
  appendColumnChildren(toDoTasks, document.getElementById('TODO'))
  appendColumnChildren(inProgressTasks, document.getElementById('IN PROGRESS'))
  appendColumnChildren(doneTasks, document.getElementById('DONE'))
}

columns.forEach(dropArea => {
  dropArea.addEventListener('dragover', async event => {
    event.preventDefault()
    const afterElement = getDragAfterElement(dropArea, event.clientY)
    const draggable = document.querySelector('.dragging')
    if (afterElement == null) {
      dropArea.appendChild(draggable)
    } else {
      dropArea.insertBefore(draggable, afterElement)
    }
  });
});


function getDragAfterElement(dropArea, y) {
  const draggableElements = [...dropArea.querySelectorAll('.draggable:not(.dragging)')]
  
  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect()
    const offset = y - box.top - box.height / 2
    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child }
    } else {
      return closest
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element
}

function formatLocalISOFromString(dateUTCString) {
  const dateTime = new Date(dateUTCString);
  const timeZoneOffSet = dateTime.getTimezoneOffset() * 60 * 1000;
  let dateTimeLocal = dateTime - timeZoneOffSet;
  dateTimeLocal = new Date(dateTimeLocal);
  let iso = dateTimeLocal.toISOString();
  iso = iso.split('.')[0];
  iso = iso.replace('T', ' ');
  return iso;
}

function getValidDateISOString(dateLocalStr) {
  if(dateLocalStr !== "") {
    return new Date(dateLocalStr).toISOString()
  }
  let defaultDate =  new Date()
  defaultDate.setHours(0,0,0,0)
  defaultDate.setDate(defaultDate.getDate() + 1)
  return defaultDate.toISOString()
}

function getValidEstimatedTime(time) {
  if(time === "") {
    return 0;
  }
  return Number(time);
}

renderColumns()

deleteBtn.addEventListener('click', async () => {
  await fetch(`/api/tasks/${currentTaskID}/`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
    }
  });
  renderColumns();
})

editBtn.addEventListener('click', () => {
  if(editBtn.value === 'Edit'){
    toggleOffcanvasFields(true);
    editBtn.value = 'Done';
  }
  else{
    toggleOffcanvasFields(false);
    updateTask();
    editBtn.value = 'Edit'
  }
})

createBtn.addEventListener('click', async () => {
  await fetch('/api/tasks/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    body: JSON.stringify({
      'title': taskModalTitle.value,
      'start': getValidDateISOString(taskModalEndDate.value),
      'taskboard': taskboardID,
      'status': taskModalStatus.value,
      'details': taskModalDetails.value,
      'time_estimate': getValidEstimatedTime(taskModalET.value)
    })
  });
  createTaskModal.hide();
  renderColumns();
});

document.getElementById('addTask').addEventListener('hidden.bs.modal', () => {
  taskModalTitle.value = '';
  taskModalEndDate.value = '';
  taskModalET.value = '';
  taskModalStatus.selectedIndex = 0;
  taskModalDetails.value = '';
});