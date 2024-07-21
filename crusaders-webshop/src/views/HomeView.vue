<template>
  <main>
    <Toast />
    <Button label="Admin" @click="onClickAdmin" />
    <Dialog v-model:visible="showModal" modal header="Logga in">
      <div class="login-container">
        <div class="input-otp-container">
          <InputOtp v-model="pinCode" :length="6" mask integerOnly />
          <Button
            :disabled="emptyPinCode"
            severity="danger"
            icon="pi pi-delete-left"
            @click="deleteInput"
          />
        </div>

        <KeyPad @handle-pin-code-input="handlePinCodeInput" />
        <p v-if="showError" class="error-message">{{ errorMessage }}</p>
      </div>
    </Dialog>

    <UserList />
  </main>
</template>

<script>
import UserList from '../components/users/UserList.vue';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputOtp from 'primevue/inputotp';
import store from '@/store';
import router from '@/router';
import KeyPad from '@/components/KeyPad.vue';
import axios from 'axios';
import Toast from 'primevue/toast';

export default {
  name: 'HomeView',
  components: {
    KeyPad,
    UserList,
    Button,
    Dialog,
    InputOtp,
    Toast
  },
  data() {
    return {
      showModal: false,
      pinCode: null,
      showError: false,
      errorMessage: ''
    };
  },
  watch: {
    async pinCode() {
      if (this.pinCode.length === 6) {
        try {
          const response = await axios.post('http://127.0.0.1:5000/login-admin', {
            pinCode: this.pinCode
          });

          if (response.status === 200) {
            await store.dispatch('loginAdmin');
            this.closeModal();
            await router.push({ path: '/admin' });
          }
        } catch (e) {
          if (e.response.status === 401) {
            this.errorMessage = 'Fel pinkod';
          } else {
            this.$toast.add({
              severity: 'error',
              summary: 'Något gick fel',
              detail: 'Skrik på Adam',
              life: 6000
            });
          }
          this.showError = true;
        }
        this.pinCode = '';
      } else if (this.pinCode && this.pinCode.length > 0) {
        this.showError = false;
      }
    }
  },
  computed: {
    emptyPinCode() {
      return !this.pinCode;
    }
  },
  methods: {
    onClickAdmin() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    deleteInput() {
      if (this.pinCode.length > 0) {
        this.pinCode = this.pinCode.slice(0, -1);
      }
    },
    handlePinCodeInput(number) {
      if (!this.pinCode) {
        this.pinCode = number;
      } else {
        this.pinCode += number;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 30px;
}

.input-otp-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 30px;
}

.error-message {
  color: red;
}
</style>
