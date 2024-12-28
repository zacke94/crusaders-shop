<template>
  <Toast />
  <Button label="Öppna kyl" @click="onClickOpenFridge"></Button>
  <Dialog
    v-model:visible="showModal"
    header="Kylen är öppen"
    modal
    :style="{ 'min-width': '400px' }"
  >
    <h3>🚨🚨 GLÖM INTE ATT LÅSA KYL 🚨🚨</h3>
    <Button class="mt-16" label="Lås kyl" @click="onClickCloseFridge"></Button>
  </Dialog>
</template>

<script>
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import Toast from 'primevue/toast';
import FridgeService from '@/services/fridge-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'OpenFridgeModal',
  components: {
    Button,
    Dialog,
    Toast
  },
  data() {
    return {
      showModal: false,
      isLoading: false,
      errorMsg: ''
    };
  },
  methods: {
    async onClickOpenFridge() {
      try {
        await FridgeService.unlockFridge({ isAdmin: true });
        this.showModal = true;
      } catch {
        ToastService.showError(this.$toast);
      }
    },
    async onClickCloseFridge() {
      try {
        await FridgeService.lockFridge();
        this.showModal = false;
      } catch {
        ToastService.showError(this.$toast);
      }
    }
  }
};
</script>
