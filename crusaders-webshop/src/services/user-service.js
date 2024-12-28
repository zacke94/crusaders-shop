import axios from 'axios';
import { User } from '@/models/User';
import { noEmptyList } from '@/utils/list-utils';

const API_BASE_URL = 'http://127.0.0.1:5000';

const UserService = {
  /**
   * @param {number} userId
   * @returns {Promise<User>}
   */
  async getUser(userId) {
    const response = await axios.get(`${API_BASE_URL}/user/${userId}`);
    if (response.data) {
      return new User(response.data);
    }
  },

  /**
   * @returns {Promise<User[]|[]>}
   */
  async getActiveUsers() {
    const response = await axios.get(`${API_BASE_URL}/active-users`);
    if (noEmptyList(response.data.users)) {
      return response.data.users.map((user) => new User(user));
    }
    return [];
  },

  /**
   * @returns {Promise<User[]|[]>}
   */
  async getAllUsers() {
    const response = await axios.get(`${API_BASE_URL}/all-users`);
    if (noEmptyList(response.data.users)) {
      return response.data.users.map((user) => new User(user));
    }
    return [];
  },

  /**
   * @param {*} request
   * @returns {Promise<void>}
   */
  async loginUser(request) {
    await axios.post(`${API_BASE_URL}/login-user`, request);
  },

  /**
   * @param {number} userId
   * @return {Promise<void>}
   */
  async activateUser(userId) {
    await axios.put(`${API_BASE_URL}/activate-user/${userId}`);
  },

  /**
   * @param {number} userId
   * @returns {Promise<void>}
   */
  async inactivateUser(userId) {
    await axios.put(`${API_BASE_URL}/inactivate-user/${userId}`);
  },

  /**
   * @param {User[]} users
   * @returns {Promise<void>}
   */
  async addUsers(users) {
    await axios.post(`${API_BASE_URL}/add-users`, users);
  },

  /**
   * @param {Object} requestData
   * @returns {Promise<void>}
   */
  async changePinCode(requestData) {
    await axios.put(`${API_BASE_URL}/change-pin-code`, requestData);
  }
};

export default UserService;
