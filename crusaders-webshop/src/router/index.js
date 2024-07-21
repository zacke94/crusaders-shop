import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ConfirmOrderView from '../components/modals/ConfirmOrderModal.vue';
import SuccessfulOrderView from '@/views/SuccessfulOrderView.vue';
import AdminView from '../views/admin/AdminView.vue';
import ManageUsersView from '@/views/admin/ManageUsersView.vue';
import ManageProductsView from '@/views/admin/ManageProductsView.vue';
import ShowOrdersView from '@/views/admin/ShowOrdersView.vue';
import UserView from '@/views/UserView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView
    },
    {
      path: '/user/:userId',
      component: UserView,
      props: true
    },
    {
      path: '/buy-products/:userId/confirm-orderProducts',
      component: ConfirmOrderView,
      props: true
    },
    {
      path: '/successful-order/:userId',
      component: SuccessfulOrderView,
      props: true
    },
    {
      path: '/admin',
      children: [
        {
          path: '',
          component: AdminView
        },
        {
          path: 'manage-users',
          component: ManageUsersView
        },
        {
          path: 'manage-products',
          component: ManageProductsView
        },
        {
          path: 'show-orders',
          component: ShowOrdersView
        }
      ]
    }
  ]
});

export default router;
