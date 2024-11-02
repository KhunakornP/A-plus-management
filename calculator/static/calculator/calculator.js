async function fetchExamFieldsJSON() {
  const tgatResponse = await fetch('/api/exams/?exam_type=TGAT');
  const tgat = await tgatResponse.json();
  return tgat;
}

function generateExamFields(exam){
  const examField = document.createElement('div')
  examField.innerHTML = `
  <div class="card-body" style="width: 250px">
        <label for="${exam.name}">${exam.name}</label>
        <input class="form-control" aria-describedby="${exam.name}-help" id="${exam.name}" placeholder="${exam.max_score}">
        <small id="${exam.name}-help" class="form-text text-muted">สูงสุด ${exam.max_score}</small>
      </div>
  `
  return examField;
}

const examFieldContainer = document.getElementById('exam-field-container')

async function appendExams(exams) {
  for (const exam of exams) {
    examFieldContainer.appendChild(generateExamFields(exam));
  }
}

async function renderExams() {
  const exams = await fetchExamFieldsJSON();
  appendExams(exams);
}

document.addEventListener('DOMContentLoaded', async () => {
    renderExams();
  })
