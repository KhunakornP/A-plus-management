async function fetchTaskboardJSON() {
let studentID;
  if (document.getElementById('student_id')) {
  studentID = JSON.parse(document.getElementById('student_id').textContent);
  console.log(studentID);
  } else {
  studentID = '';
  }
  const response = await fetch(`/api/taskboards/?user_id=${studentID}`)
  const taskboards = await response.json();
  return taskboards;
}

function generateTaskboardCard(taskboard) {
  const card = document.createElement('div');
  card.classList.add('col-lg-4', 'col-md-6', 'mb-4');
  card.innerHTML = `
    <div class="card h-100 bg-light-subtle border-0 shadow-lg rounded-lg overflow-hidden" id="taskboard-${taskboard.id}">
      <div class="card-header bg-warning text-white text-center py-4">
          <h4 class="mb-0"> ${taskboard.name}</h4>
      </div>
      <div class="card-body">
        <div class="d-grid gap-2 d-md-block">
            <a href="/manager/taskboard/${taskboard.id}/" class="btn btn-info mx-2">Go to board</a>
            <button class="btn btn-danger mx-2 delete-btn" id=${taskboard.id}>Delete</button>
        </div>
      </div>
    </div>
  `;
  return card;
}

const taskboardContainer = document.getElementById('taskboard-container');

async function appendTaskboards(taskboards) {
  for (const taskboard of taskboards) {
    taskboardContainer.appendChild(generateTaskboardCard(taskboard));
  }
}

async function renderTaskboards() {
  taskboardContainer.innerHTML = '';
  const taskboards = await fetchTaskboardJSON();
  if (taskboards.length !== 0) {
    appendTaskboards(taskboards);
  } else {
    const noTaskboardMessage =
      '<h4 class="text-white text-center">You have no taskboard</h4>';
    document.getElementById('taskboard-container').innerHTML =
      noTaskboardMessage;
  }
  bindDeleteButtons();
}

async function bindDeleteButtons() {
  const buttons = document.querySelectorAll('.delete-btn');
  buttons.forEach((btn) => {
    btn.addEventListener('click', async () => {
      await fetch('/api/taskboards/'.concat(btn.id).concat('/'), {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
      });
      renderTaskboards();
    });
  });
}

document.addEventListener('DOMContentLoaded', async () => {
  await renderTaskboards();
  const btn = document.getElementById('create-tb-btn');
  const userID = JSON.parse(document.getElementById('user_id').textContent);
  btn.addEventListener('click', async () => {
    await fetch('/api/taskboards/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        'name': document.getElementById('taskboard-title').value,
        'user': userID,
      }),
    });
    renderTaskboards();
  });
});
