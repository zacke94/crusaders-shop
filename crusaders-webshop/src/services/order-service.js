import axios from 'axios';
import { noEmptyList } from '@/utils/list-utils';
import { Order } from '@/models/Order';

const API_BASE_URL = 'http://127.0.0.1:5000';

const OrderService = {
  /**
   * @returns {Promise<Order[]|[]>}
   */
  async getOrders() {
    const response = await axios.get(`${API_BASE_URL}/get-orders`);
    if (noEmptyList(response.data)) {
      return response.data.map((order) => new Order(order));
    }
    return [];
  },

  /**
   * @param {number} userId
   * @returns {Promise<Order[]|[]>}
   */
  async getOrder(userId) {
    const response = await axios.get(`${API_BASE_URL}/get-order/${userId}`);
    if (noEmptyList(response.data)) {
      return response.data.map((order) => new Order(order));
    }
    return [];
  },

  /**
   * @param {Order} order
   * @returns {Promise<number>} orderId
   */
  async addOrder(order) {
    const response = await axios.post(`${API_BASE_URL}/add-order`, order);
    return response.data.orderId;
  }
};

export default OrderService;
