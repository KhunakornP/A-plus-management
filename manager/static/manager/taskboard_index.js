async function fetchTaskboardJSON() {
  const response = await fetch('/manager/api/taskboard/');
  const taskboards = await response.json();
  return taskboards;
}
// {% url 'manager:taskboard' taskboard.id %}
// {% url 'manager:delete_taskboard' taskboard.id %}

function generateTaskboardCard(taskboard) {
  const card = document.createElement('div');
  card.classList.add('col-lg-4', 'col-md-6', 'mb-4');
  card.innerHTML = `
    <div class="card h-100 bg-light-subtle border-0 shadow-lg rounded-lg overflow-hidden">
      <div class="card-header bg-warning text-white text-center py-4">
          <h4 class="mb-0"> ${taskboard.name}</h4>
      </div>
      <div class="card-body">
        <div class="d-grid gap-2 d-md-block">
        <a href="#" class="btn btn-info mx-2">Go to board</a>
            <a href="#" class="btn btn-danger mx-2">Delete</a>
        </div>
      </div>
    </div>
  `;

  return card;
}

async function appendTaskboards(taskboards) {
  const page = document.getElementById('taskboard-container')
  for (const taskboard of taskboards) {
    page.appendChild(generateTaskboardCard(taskboard));
  }
}

document.addEventListener('DOMContentLoaded', async ()=>{
  const taskboards = await fetchTaskboardJSON()
  if (taskboards!== null) {
    appendTaskboards(taskboards)
  }
  else {
    const noTaskboardMessage = '<h4 class="text-white text-center">You have no taskboard</h4>'
    document.getElementById('taskboard-container').innerHTML = noTaskboardMessage
  }
})

