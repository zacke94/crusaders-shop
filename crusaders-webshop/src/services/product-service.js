import axios from 'axios';
import { noEmptyList } from '@/utils/list-utils';
import { Product } from '@/models/Product';

const API_BASE_URL = 'http://127.0.0.1:5000';

const ProductService = {
  /**
   * @returns {Promise<Product[]|[]>}
   */
  async getEligibleProducts() {
    const response = await axios.get(`${API_BASE_URL}/eligible-products`);

    if (noEmptyList(response.data.products)) {
      return response.data.products.map(
        (product) =>
          new Product({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: product.quantity
          })
      );
    }
    return [];
  },

  /**
   * @returns {Promise<Product[]|[]>}
   */
  async getAllProducts() {
    const response = await axios.get(`${API_BASE_URL}/all-products`);

    if (noEmptyList(response.data.products)) {
      return response.data.products.map(
        (product) =>
          new Product({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: product.quantity,
            showProduct: product.showProduct
          })
      );
    }
    return [];
  },

  /**
   * @param {Product} product
   * @returns {Promise<void>}
   */
  async addProduct(product) {
    await axios.post(`${API_BASE_URL}/add-product`, product);
  },

  /**
   * @param {Product} product
   * @returns {Promise<void>}
   */
  async editProduct(product) {
    await axios.put(`${API_BASE_URL}/edit-product`, product);
  },

  /**
   * @param {number} productId
   * @returns {Promise<void>}
   */
  async hideProduct(productId) {
    await axios.put(`${API_BASE_URL}/hide-product/${productId}`);
  },

  /**
   * @param {number} productId
   * @returns {Promise<void>}
   */
  async showProduct(productId) {
    await axios.put(`${API_BASE_URL}/show-product/${productId}`);
  }
};

export default ProductService;
