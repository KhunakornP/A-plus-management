class AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    this.Containers = {
      'aptitude': tContainer,
      'aLevel': aContainer,
      'other': oContainer,
    };
  }

  // abstract methods
  /* eslint-disable */

  async fetchCardContentJSON(examType) {
    const response = await fetch(`/api/exams/?exam_type=${examType}`);
    const exams = await response.json();
    return exams;
  }

  async fetchSavedDataJSON(examID) {
    throw new Error('Not Implemented');
  }
  generateCards(exam, savedValue) {
    throw new Error('Not Implemented');
  }
  async save() {
    throw new Error('Not Implemented');
  }
  async saveOne(examID, score) {
    throw new Error('Not Implemented');
  }
  async redirect() {
    throw new Error('Not Implemented');
  }

  async generateAndAppendCards(children, parent) {}
  /* eslint-enable */

  async renderContent() {
    const tgat = await this.fetchCardContentJSON('TGAT');
    const tpat = await this.fetchCardContentJSON('TPAT');
    const aLevels = await this.fetchCardContentJSON('A-Level');
    const others = await this.fetchCardContentJSON('Other');
    await this.generateAndAppendCards(tgat, this.Containers.aptitude);
    await this.generateAndAppendCards(tpat, this.Containers.aptitude);
    await this.generateAndAppendCards(aLevels, this.Containers.aLevel);
    await this.generateAndAppendCards(others, this.Containers.other);
  }
}

export { AbstractExamFields };
