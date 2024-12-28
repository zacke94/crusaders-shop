import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

const FridgeService = {
  /**
   * @returns {Promise<void>}
   */
  async lockFridge() {
    await axios.post(`${API_BASE_URL}/lock-fridge`);
  },

  /**
   * @param {Object} requestData
   * @returns {Promise<void>}
   */
  async unlockFridge(requestData) {
    await axios.post(`${API_BASE_URL}/unlock-fridge`, requestData);
  }
};

export default FridgeService;
