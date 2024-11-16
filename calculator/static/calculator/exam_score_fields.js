import { AbstractExamFields } from "./abstract_exam_fields.js";

class ExamScoreFields extends AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    super(tContainer, aContainer, oContainer);
  }

  async fetchExamsJSON(examType) {
    const response = await fetch(`/api/exams/?exam_type=${examType}`);
    const exams = await response.json();
    return exams;
  }

  generateExamCards(exam) {
    const examField = document.createElement('div');
    examField.innerHTML = `
    <div class="card-body">
          <label for="${exam.name}">${exam.name}</label>
          <input class="form-control exam-field" id="${exam.name}" placeholder="${exam.max_score}">
          <small id="${exam.name}-help" class="form-text text-muted">สูงสุด ${exam.max_score}</small>
        </div>
    `;
    return examField;
  }
}

export { ExamScoreFields };
