<template>
  <!-- TODO: change exclamation mark -->
  <div v-if="adminIsAuthenticated">
    <Button label="Logga ut" @click="onClickLogout"></Button>

    <h1>Admin gränssnitt</h1>
    <Button label="Hantera användare" @click="onClickManageUsers"></Button>
    <Button label="Hantera produkter" @click="onClickManageProducts"></Button>
    <Button label="Visa ordrar" @click="onClickShowOrders"></Button>
    <OpenFridgeModal />
  </div>
  <div v-else>
    <h1>Not authenticated</h1>
  </div>
</template>

<script>
import { storeMixin } from '@/mixins/store-mixin';
import Button from 'primevue/button';
import store from '@/store';
import router from '@/router';
import OpenFridgeModal from '@/components/modals/OpenFridgeModal.vue';

export default {
  name: 'AdminView',
  mixins: [storeMixin],
  components: {
    OpenFridgeModal,
    Button
  },
  data() {
    return {
      id: null
    };
  },
  methods: {
    onClickEditPinCode(id) {
      this.id = id;
      this.showEditPinCodeModal = true;
    },
    async onClickLogout() {
      await store.dispatch('logoutAdmin');
      await router.push({ path: '/' });
    },
    async onClickManageUsers() {
      await router.push({ path: '/admin/manage-users' });
    },
    async onClickManageProducts() {
      await router.push({ path: '/admin/manage-products' });
    },
    async onClickShowOrders() {
      await router.push({ path: '/admin/show-orders' });
    }
  }
};
</script>
