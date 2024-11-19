import { ExamWeightFields } from './exam_weight_fields.js';
let currentCriteriaID = 0;

async function fetchUniversities() {
  const response = await fetch('/api/universities/');
  const universities = await response.json();
  return universities;
}

async function fetchFaculties(universityID) {
  const response = await fetch(`/api/faculties/?university=${universityID}`);
  const faculties = await response.json();
  return faculties;
}

async function fetchMajors(facultyID) {
  const response = await fetch(`/api/majors/?faculty=${facultyID}`);
  const majors = await response.json();
  return majors;
}

async function fetchCriteriaSet(majorID) {
  const response = await fetch(`/api/criteria/?major=${majorID}`);
  const criteriaSet = await response.json();
  return criteriaSet;
}

function addSelectOptions(selectElement, data) {
  data.forEach((entry) => {
    const option = document.createElement('option');
    option.value = entry.id;
    option.innerHTML = entry.name;
    selectElement.appendChild(option);
  });
}

function removeSelectOptions(selectElement) {
  let i,
    L = selectElement.options.length - 1;
  for (i = L; i >= 1; i--) {
    selectElement.remove(i);
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const examContainer = new ExamWeightFields(
    document.getElementById('tgat-tpat'),
    document.getElementById('a-level'),
    document.getElementById('other-exams')
  );
  await examContainer.renderContent();

  const universitySelect = document.getElementById('university');
  const facultySelect = document.getElementById('faculty');
  const majorSelect = document.getElementById('major');
  const criteriaSelect = document.getElementById('criteria');
  const resultsButton = document.getElementById('results-btn');
  const universities = await fetchUniversities();
  const weightInputs = document.querySelectorAll('.exam-weight-input');
  let criteria;
  addSelectOptions(universitySelect, universities);

  universitySelect.addEventListener('change', async () => {
    removeSelectOptions(facultySelect);
    removeSelectOptions(majorSelect);
    removeSelectOptions(criteriaSelect);
    const faculties = await fetchFaculties(universitySelect.value);
    addSelectOptions(facultySelect, faculties);
  });

  facultySelect.addEventListener('change', async () => {
    removeSelectOptions(majorSelect);
    removeSelectOptions(criteriaSelect);
    const majors = await fetchMajors(facultySelect.value);
    addSelectOptions(majorSelect, majors);
  });

  majorSelect.addEventListener('change', async () => {
    removeSelectOptions(criteriaSelect);
    criteria = await fetchCriteriaSet(majorSelect.value);
    addSelectOptions(criteriaSelect, criteria);
  });

  criteriaSelect.addEventListener('change', () => {
    currentCriteriaID = criteriaSelect.value;
    console.log(currentCriteriaID);
    examContainer.insertScoreWeight(currentCriteriaID);
  });

  resultsButton.addEventListener('click', async () => {
    const weightData = Array.from(weightInputs, (input) => {
      return { 'weight': input.value, 'exam': input.id };
    });
    const response = await fetch('/api/exam_score/calculate_score/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        criteria: weightData,
      }),
    });
    window.location = response.url;
  });
});
