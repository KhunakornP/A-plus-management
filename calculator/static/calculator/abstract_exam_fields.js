class AbstractExamFields {
  constructor(tContainer, aContainer, oContainer) {
    this.Containers = {
      'aptitude': tContainer,
      'aLevel': aContainer,
      'other': oContainer,
    };
    this.userID = JSON.parse(document.getElementById('user_id').textContent);
  }

  async fetchCardContentJSON(examType) {}
  async fetchSavedValueJSON(exam) {}
  generateCards(exam) {}
  async save() {}
  async saveOne(examID, score) {}
  redirect() {}

  generateAndAppendCards(children, parent) {
    if (parent !== null) {
      for (const child of children) {
        parent.appendChild(this.generateCards(child));
      }
    }
  }

  async renderContent() {
    const tgat = await this.fetchCardContentJSON('TGAT');
    const tpat = await this.fetchCardContentJSON('TPAT');
    const aLevels = await this.fetchCardContentJSON('A-Level');
    const others = await this.fetchCardContentJSON('Other');
    this.generateAndAppendCards(tgat, this.Containers.aptitude);
    this.generateAndAppendCards(tpat, this.Containers.aptitude);
    this.generateAndAppendCards(aLevels, this.Containers.aLevel);
    this.generateAndAppendCards(others, this.Containers.other);
  }
}

export { AbstractExamFields };
