export class User {
  constructor({ id = 0, name = '', pinCode = null } = {}) {
    this.id = id;
    this.name = name;
    this.pinCode = pinCode;
  }
}
