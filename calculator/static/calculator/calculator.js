import { ExamScoreFields } from './exam_score_fields.js';
import { preventNonNumeric } from './abstract_exam_fields.js';

document.addEventListener('DOMContentLoaded', async () => {
  const examContainers = new ExamScoreFields(
    document.getElementById('tgat-tpat'),
    document.getElementById('a-level'),
    document.getElementById('other-exams')
  );
  await examContainers.renderContent();
  document.getElementById('save-btn').addEventListener('click', async () => {
    examContainers.save();
  });
  document
    .getElementById('continue-btn')
    .addEventListener('click', async () => {
      examContainers.redirect();
    });

  const scoreInput = document.querySelectorAll('.form-control');
  scoreInput.forEach((input) => {
    input.addEventListener('keydown', preventNonNumeric);
  });
});
