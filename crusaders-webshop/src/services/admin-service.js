import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const AdminService = {
  /**
   * @param {Object} requestData
   * @returns {Promise<void>}
   */
  async loginAdmin(requestData) {
    await axios.post(`${API_BASE_URL}/login-admin`, requestData);
  }
};

export default AdminService;
