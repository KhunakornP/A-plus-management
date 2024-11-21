async function fetchScoreHistory(query) {
  const response = await fetch(`/api/score_history/?${query}`);
  const scoreHistories = await response.json();
  return scoreHistories[0];
}

async function fetchExam(examID) {
  const response = await fetch(`/api/exams/${examID}`);
  const exams = await response.json();
  return exams;
}

async function fetchCriteria(criteriaID) {
  const response = await fetch(`/api/criteria/${criteriaID}`);
  const criteria = await response.json();
  return criteria;
}

async function createMinCriteriaCard(criteriaObj) {
  const card = document.createElement('div');
  const exam = await fetchExam(Number(criteriaObj.exam));
  card.innerHTML = `${exam.name}: ${criteriaObj.min_score}`;
  return card;
}

async function createMultipleMinCriteriaCards(children, parent) {
  for (const child of children) {
    parent.appendChild(await createMinCriteriaCard(child));
  }
}

function getMyTcasLink(majorCode) {
  return 'https://course.mytcas.com/programs/' + majorCode;
}

document.addEventListener('DOMContentLoaded', async () => {
  const minCriteriaDiv = document.querySelector('.min-criteria');
  const criteriaID = Number(minCriteriaDiv.id);
  if (criteriaID !== 0) {
    const criteria = await fetchCriteria(Number(minCriteriaDiv.id));
    createMultipleMinCriteriaCards(criteria.criteria, minCriteriaDiv);
    const statistics = await fetchScoreHistory(`criteria_set=${criteriaID}`);

    document.getElementById('min-score').innerHTML =
      `Minimum Score: ${statistics.min_score}`;
    document.getElementById('max-score').innerHTML =
      `Maximum Score: ${statistics.max_score}`;
    document.getElementById('max-seat').innerHTML =
      `Total Seats: ${statistics.max_seat}`;
    document.getElementById('register').innerHTML =
      `Applicants: ${statistics.register}`;
    document.getElementById('admitted').innerHTML =
      `Admitted: ${statistics.admitted}`;
  }
  const majorCode = document.querySelector('.mytcas-link-container').id;
  if (majorCode !== '') {
    document.getElementById('my-tcas-link').href = getMyTcasLink(majorCode);
  }
});
