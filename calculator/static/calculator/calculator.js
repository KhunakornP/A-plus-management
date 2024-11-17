import { ExamScoreFields } from './exam_score_fields.js';

document.addEventListener('DOMContentLoaded', async () => {
  const examContainers = new ExamScoreFields(
    document.getElementById('tgat-tpat'),
    document.getElementById('a-level'),
    document.getElementById('other-exams')
  );
  examContainers.renderContent();
  document.getElementById('save-btn').addEventListener('click', async () => {
    examContainers.save();
  });
  document
    .getElementById('continue-btn')
    .addEventListener('click', async () => {
      examContainers.redirect();
    });
});
