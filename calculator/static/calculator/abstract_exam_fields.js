class AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    this.examContainers = {
      'aptitude': tContainer,
      'aLevel': aContainer,
      'other': oContainer,
    };
  }

  async fetchExamsJSON(examType) {}
  generateExamCards(exam) {}
  save() {}
  saveAndRedirect() {}

  generateAndAppendExamCards(children, parent) {
    if (parent !== null) {
      for (const child of children) {
        parent.appendChild(this.generateExamCards(child));
      }
    }
  }

  async renderExams() {
    const tgat = await this.fetchExamsJSON('TGAT');
    const tpat = await this.fetchExamsJSON('TPAT');
    const aLevels = await this.fetchExamsJSON('A-Level');
    const others = await this.fetchExamsJSON('Other');
    this.generateAndAppendExamCards(tgat, this.examContainers.aptitude);
    this.generateAndAppendExamCards(tpat, this.examContainers.aptitude);
    this.generateAndAppendExamCards(aLevels, this.examContainers.aLevel);
    this.generateAndAppendExamCards(others, this.examContainers.other);
  }
}

export { AbstractExamFields };
