const TContainer = document.getElementById('tgat-tpat')
const AContainer = document.getElementById('a-level')
const OContainer = document.getElementById('other-exams')


function processAndAppend(children, parent, func) {
  if (parent !== null) {
    for (const child of children) {
      parent.appendChild(func(child));
    }
  }
}

async function fetchExamFieldsJSON(examType) {
  const response = await fetch(`/api/exams/?exam_type=${examType}`);
  const exams = await response.json();
  return exams;
}

function generateExamFields(exam){
  const examField = document.createElement('div')
  examField.innerHTML = `
  <div class="card-body">
        <label for="${exam.name}">${exam.name}</label>
        <input class="form-control exam-field" id="${exam.name}" placeholder="${exam.max_score}">
        <small id="${exam.name}-help" class="form-text text-muted">สูงสุด ${exam.max_score}</small>
      </div>
  `
  return examField;
}

async function renderExams() {
  const tgat = await fetchExamFieldsJSON('TGAT');
  const tpat = await fetchExamFieldsJSON('TPAT');
  const aLevels = await fetchExamFieldsJSON('A-Level');
  const others = await fetchExamFieldsJSON('Other');
  processAndAppend(tgat, TContainer, generateExamFields);
  processAndAppend(tpat, TContainer, generateExamFields);
  processAndAppend(aLevels, AContainer, generateExamFields);
  processAndAppend(others, OContainer, generateExamFields);
}



document.addEventListener('DOMContentLoaded', async () => {
    renderExams();
})
