export class Product {
  constructor({ id = 0, balance, name, price, quantity = 0, showProduct = true } = {}) {
    this.id = id;
    this.balance = balance;
    this.name = name;
    this.price = price;
    this.quantity = quantity;
    this.totalPrice = price * quantity;
    this.showProduct = showProduct;
  }
}
