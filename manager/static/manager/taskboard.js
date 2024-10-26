const columns = document.querySelectorAll('.drop_area')
const offcanvas = new bootstrap.Offcanvas('#task-offcanvas')
const deleteBtn = document.getElementById('del-task-btn')
const editBtn = document.getElementById('edit-task-btn')
const taskOffcanvasTitle = document.getElementById('task-title')
const taskOffcanvasDetails = document.getElementById('task-details');
const taskOffcanvasEndDate = document.getElementById('task-enddate');
const taskboardID = window.location.href.split('/').slice(-2)[0];

deleteBtn.addEventListener('click', async () => {
  await fetch(`/api/tasks/${deleteBtn.value}/`, {
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

async function updateTask(){
  await fetch(`/api/tasks/${deleteBtn.value}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken')
    },
    body: JSON.stringify({
      'title': taskOffcanvasTitle.value,
      'details': taskOffcanvasDetails.value,
      'end_date': new Date(taskOffcanvasEndDate.value).toISOString()
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
  }
  else {
    taskOffcanvasTitle.setAttribute('readonly', true);
    taskOffcanvasTitle.setAttribute('class', 'form-control-plaintext');
    taskOffcanvasDetails.setAttribute('readonly', true);
    taskOffcanvasDetails.setAttribute('class', 'form-control-plaintext');
    taskOffcanvasEndDate.setAttribute('readonly', true);
    taskOffcanvasEndDate.setAttribute('class', 'form-control-plaintext');
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
    taskOffcanvasTitle.value = `${task.title}`;
    deleteBtn.value = `${task.id}`;
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
    card.classList.add('dragging');
  });

  card.addEventListener('dragend', () => {
    card.classList.remove('dragging');
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
  appendColumnChildren(toDoTasks, document.getElementById('todo'))
  appendColumnChildren(inProgressTasks, document.getElementById('in-progress'))
  appendColumnChildren(doneTasks, document.getElementById('done'))
}

columns.forEach(dropArea => {
  dropArea.addEventListener('dragover', event => {
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


renderColumns()