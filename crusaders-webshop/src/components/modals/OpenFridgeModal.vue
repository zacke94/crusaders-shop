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
    <Button style="margin-top: 16px" label="Lås kyl" @click="onClickCloseFridge"></Button>
  </Dialog>
</template>

<script>
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import axios from 'axios';
import Toast from 'primevue/toast';

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
        const response = await axios.post('http://127.0.0.1:5000/unlock-fridge', {
          isAdmin: true
        });
        if (response.status === 200) {
          this.showModal = true;
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
    },
    async onClickCloseFridge() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/lock-fridge');
        if (response.status === 200) {
          this.showModal = false;
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
    }
  }
};
</script>
