export class User {
  constructor({ id = 0, name = '', pinCode = null, isActive = true } = {}) {
    this.id = id;
    this.name = name;
    this.pinCode = pinCode;
    this.isActive = isActive;
  }
}
