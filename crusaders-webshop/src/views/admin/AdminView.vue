<template>
  <div v-if="adminIsAuthenticated">
    <Button label="Logga ut" @click="onClickLogout"></Button>

    <div class="mt-32">
      <h1>Admin gränssnitt</h1>
      <div class="mt-16 buttons-grid">
        <Button label="Hantera användare" @click="onClickManageUsers"></Button>
        <Button label="Hantera produkter" @click="onClickManageProducts"></Button>
        <Button label="Hantera ordrar" @click="onClickManageOrders"></Button>
        <OpenFridgeModal />
      </div>
    </div>
  </div>
  <div v-else>
    <h1>Inte inloggad</h1>
    <Button label="Gå till startsida" class="mt-32" @click="onClickGoHome"></Button>
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
    async onClickManageOrders() {
      await router.push({ path: '/admin/manage-orders' });
    },
    async onClickGoHome() {
      await router.push({ path: '/' });
    }
  }
};
</script>
