export class User {
  constructor({ id = 0, name = '', admin = false } = {}) {
    this.id = id;
    this.name = name;
    this.admin = admin;
  }
}
