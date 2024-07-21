export class Order {
  constructor({ customerId, customerName, orderDate, orderId, totalPrice, products} = {}) {
    this.customerId = customerId;
    this.customerName = customerName;
    this.orderDate = orderDate;
    this.orderId = orderId;
    this.totalPrice = totalPrice;
    this.products = products;
  }
}
