const columns = document.querySelectorAll('.drop_area')
const offcanvas = document.getElementById('task-offcanvas')

async function fetchTasksJSON() {
  const response = await fetch('/api/tasks/');
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
  innerCard.innerHTML = `${task.title}`
  innerCard.addEventListener('click', () => {
    console.log('clicked')
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
      // console.log(child.title)
      column.appendChild(generateTaskCard(child));
    }
  }
}

async function renderColumns() {
  const tasks = await fetchTasksJSON()
  const toDoTasks = tasks.filter(task => task.status === 'TODO')
  const inProgressTasks = tasks.filter(task => task.status === 'IN PROGRESS')
  const doneTasks = tasks.filter(task => task.status === 'DONE')
  appendColumnChildren(toDoTasks, document.getElementById('todo'))
  appendColumnChildren(inProgressTasks, document.getElementById('in-progress'))
  appendColumnChildren(doneTasks, document.getElementById('done'))
}

renderColumns()

// code for drag-and-drop stuffs

function appendCardAfterDrop(dropArea, draggable) {
  const afterElement = getDragAfterElement(dropArea, event.clientY)
  if (afterElement == null) {
    dropArea.appendChild(draggable)
  } else {
    dropArea.insertBefore(draggable, afterElement)
  }
}

columns.forEach(dropArea => {
  dropArea.addEventListener('dragover', event => {
    event.preventDefault();
  });

  dropArea.addEventListener('drop', event => {
    event.preventDefault();
    const draggable = document.querySelector('.dragging');
    if (draggable) {
      appendCardAfterDrop(dropArea, draggable);
      draggable.classList.remove('dragging');
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