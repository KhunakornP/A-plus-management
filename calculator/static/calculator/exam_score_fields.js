import { AbstractExamFields } from './abstract_exam_fields.js';

class ExamScoreFields extends AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    super(tContainer, aContainer, oContainer);
  }

  async fetchCardContentJSON(examType) {
    const response = await fetch(`/api/exams/?exam_type=${examType}`);
    const exams = await response.json();
    return exams;
  }

  generateCards(exam) {
    const examField = document.createElement('div');
    examField.innerHTML = `
    <div class="card-body exam-card" id="${exam.id}">
          <label for="${exam.name}">${exam.name}</label>
          <input class="form-control" id="${exam.id}-score" placeholder="${exam.max_score}">
          <small id="${exam.name}-help" class="form-text text-muted">สูงสุด ${exam.max_score}</small>
        </div>
    `;
    return examField;
  }

  async save() {
    const examFields = document.querySelectorAll('.exam-card');
    for (const examField of examFields) {
      const examID = examField.id;
      const examScore = document.getElementById(`${examID}-score`).value;
      await this.saveOne(examID, examScore);
    }
  }

  async saveOne(exam, score) {
    await fetch('/api/exam_score/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        'student': this.userID,
        'exam': exam,
        'score': score,
      }),
    });
  }
}

export { ExamScoreFields };