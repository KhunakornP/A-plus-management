import { ExamWeightFields } from './exam_weight_fields.js';
import { preventNonNumeric } from './abstract_exam_fields.js';
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

  weightInputs.forEach((input) => {
    input.addEventListener('keydown', preventNonNumeric);
    input.addEventListener('change', () => {
      if (Number(input.value) > 100) {
        input.value = 100;
      }
    });
  });

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
    examContainer.insertScoreWeight(currentCriteriaID);
  });

  resultsButton.addEventListener('click', async () => {
    const weightData = Array.from(weightInputs, (input) => {
      return {
        'weight': input.value !== '' ? input.value : '0',
        'exam': input.id,
      };
    });

    const totalWeight = weightData.reduce((sum, item) => sum + Number(item.weight),0);
    if (totalWeight !== 100 && criteriaSelect.value === '') {
      alert(
        `The sum of the score weight must equal 100 (Current Weight: ${totalWeight})`
      );
    } else {
      const response = await fetch('/api/exam_score/calculate_score/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
          'criteria': weightData,
          'criteria_id': criteriaSelect.value !== '' ? criteriaSelect.value : 0,
          'major_id': majorSelect.value !== '' ? criteriaSelect.value : 0,
        }),
      });
      window.location = response.url;
    }
  });
});
