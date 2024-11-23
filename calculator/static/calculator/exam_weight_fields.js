import { AbstractExamFields } from './abstract_exam_fields.js';

class ExamWeightFields extends AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    super(tContainer, aContainer, oContainer);
  }

  async fetchSavedDataJSON(criteriaID) {
    const response = await fetch(`/api/criteria/${criteriaID}`);
    if (!response.ok) {
      return null;
    }
    let criteria = await response.json();
    const result = {};
    for (const obj of criteria.criteria) {
      result[obj.exam] = {
        'weight': obj.weight,
        'min_score': obj.min_score,
      };
    }
    return result;
  }

  async generateAndAppendCards(children, parent) {
    if (parent !== null) {
      for (let i = 0; i < children.length; i++) {
        const exam = children[i];
        parent.appendChild(this.generateCards(exam, 0));
      }
    }
  }

  async insertScoreWeight(criteriaID) {
    const scoreWeight = await this.fetchSavedDataJSON(criteriaID);
    const weightInputs = document.querySelectorAll('.exam-weight-input');
    for (const w of weightInputs) {
      const examID = Number((w.id).split("-")[1]);
      const weight = examID in scoreWeight ? scoreWeight[examID].weight : '';
      w.value = weight;
    }
  }

  generateCards(exam, savedValue) {
    const placeholder = 'Percentage (0-100)';
    const weightValue = savedValue ? savedValue !== 0 : '';
    const examField = document.createElement('div');
    examField.innerHTML = `
    <div class="card-body exam-card">
    <label for="${exam.name}">${exam.name}</label>
    <input type="number" min="0" max="100" class="form-control exam-weight-input" id="exam-${exam.id}" value="${weightValue}", placeholder="${placeholder}">
    </div>
    `;
    return examField;
  }

}

export { ExamWeightFields };
