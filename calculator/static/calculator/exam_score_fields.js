import { AbstractExamFields } from './abstract_exam_fields.js';

class ExamScoreFields extends AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    super(tContainer, aContainer, oContainer);
    this.maxExamScore = {};
    this.userID = JSON.parse(document.getElementById('user_id').textContent);
  }

  async fetchSavedDataJSON() {
    const response = await fetch('/api/exam_score/');
    let scores = await response.json();
    return scores.reduce(
      (index, data) => ({ ...index, [data.exam]: data }),
      {}
    );
  }

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

  async save() {
    const examFields = document.querySelectorAll('.exam-card');
    for (const examField of examFields) {
      const examID = examField.id;
      const examInput = document.getElementById(`${examID}-score`);
      const examScore = examInput.value;
      try {
        await this.saveOne(examID, examScore);
        examInput.classList.remove('is-invalid');
      } catch (error) {
        console.log(error)
        examInput.classList.add('is-invalid');
      }
    }
  }

  async saveOne(examID, score) {
    const maxScore = this.maxExamScore[examID];
    if (score > maxScore) {
      throw new Error(
        `The score of exam ${examID} cannot exceeds maximum score.`
      );
    }
    const response = await fetch('/api/exam_score/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify({
        'student': this.userID,
        'exam': examID,
        'score': score,
      }),
    });
    if (!response.ok) {
      throw new Error(
        `The score of exam ${examID} is not in a valid format.`
      );
    }
  }
  async redirect() {
    await this.save();
    const invalidInput = document.querySelectorAll('.is-invalid');
    if (invalidInput.length === 0) {
      window.location.replace(window.location.href + '2');
    }
  }
}

export { ExamScoreFields };
