import { AbstractExamFields } from './abstract_exam_fields.js';

class ExamWeightFields extends AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    super(tContainer, aContainer, oContainer);
    this.maxExamScore = {};
  }

  // TODO: change
  async fetchCardContentJSON(examType) {
    const response = await fetch(`/api/exams/?exam_type=${examType}`);
    const exams = await response.json();
    return exams;
  }

  // TODO: change
  async fetchSavedDataJSON(criteriaID) {
    // fetch this god damn thing from criteria set instead.
    // criteria is from input box
    // University -> Faculty -> Major -> Criteria
    // we may also need to addEventListener or something.
    const response = await fetch('/api/exam_score/');
    let scores = await response.json();
    return scores.reduce(
      (index, data) => ({ ...index, [data.exam]: data }),
      {}
    );
  }

  // TODO: change
  async generateAndAppendCards(children, parent) {
    if (parent !== null) {
      const userScores = await this.fetchSavedDataJSON();
      for (const exam of children) {
        let examScore = 0;
        if (exam.id in userScores) {
          examScore = userScores[exam.id].score;
        }
        parent.appendChild(this.generateCards(exam, examScore));
      }
    }
  }

  // TODO: change
  generateCards(exam, savedValue) {
    const examField = document.createElement('div');
    examField.innerHTML = `
    <div class="card-body exam-card" id="${exam.id}">
    <label for="${exam.name}">${exam.name}</label>
    <input type="number" min="0" max=${exam.max_score} class="form-control" id="${exam.id}-score" value="${savedValue}">
    <small id="${exam.name}-help" class="form-text text-muted">สูงสุด ${exam.max_score}</small>
    </div>
    `;
    this.maxExamScore[exam.id] = exam.max_score;
    return examField;
  }

  redirect() {
    // TODO: do.
  }
}

export { ExamWeightFields };
