import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/UsersView.vue';
import BuyProductsView from '../views/BuyProductsView.vue';
import ConfirmOrderView from '../components/modals/ConfirmOrderModal.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/buy-products/:userId',
      component: BuyProductsView,
      props: true
    },
    {
      path: '/buy-products/:userId/confirm-order',
      component: ConfirmOrderView,
      props: true
    }
  ]
});

export default router;
