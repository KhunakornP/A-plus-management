async function fetchScoreHistory() {
  // TODO write API view for ScoreHistory model
  await fetch()
}

async function fetchExams(query) {
  const url= `/api/exams/?${query}`
  const response = await fetch(url);
  const exams = await response.json();
  return exams;
}

function createMinCriteriaCard(examName, minScore, maxScore) {
  return `
  <div>
    ${examName}: ${minScore} ${maxScore}
  </div>
  `
}

const minCriteriaDiv = document.querySelector('.min-criteria');


document.addEventListener('DOMContentLoaded', async () => {

})