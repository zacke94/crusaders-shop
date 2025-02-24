<template>
  <div>
    <Button :label="user.name" @click="onClickOpenModal" class="user-name-button" />
    <Dialog v-model:visible="showModal" modal header="Logga in">
      <div class="login-container">
        <div class="input-otp-container">
          <InputOtp v-model="pinCode" mask integerOnly />
          <Button
            :disabled="emptyPinCode"
            severity="danger"
            icon="pi pi-delete-left"
            @click="deleteInput"
          />
        </div>
        <KeyPad @handle-pin-code-input="handlePinCodeInput" />
        <p v-if="showError" class="error-message">{{ errorMessage }}</p>
        <Toast />
      </div>
    </Dialog>
  </div>
</template>

<script>
import Dialog from 'primevue/dialog';
import InputOtp from 'primevue/inputotp';
import { User } from '@/models/User';
import router from '@/router';
import KeyPad from '@/components/KeyPad.vue';
import Button from 'primevue/button';
import store from '@/store';
import Toast from 'primevue/toast';
import UserService from '@/services/user-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'UserListItem',
  components: {
    KeyPad,
    Button,
    Dialog,
    InputOtp,
    Toast
  },
  props: {
    user: {
      type: User,
      required: true
    }
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
      if (this.pinCode.length === 4) {
        const request = {
          id: this.user.id,
          pinCode: this.pinCode
        };

        try {
          await UserService.loginUser(request);
          await store.dispatch('loginUser', this.user.id);
          this.closeModal();
          await router.push({ path: `/user/${this.user.id}` });
        } catch (e) {
          if (e.response.status === 401) {
            this.errorMessage = 'Fel pinkod';
            this.showError = true;
          } else {
            ToastService.showError(this.$toast);
          }
        }
      } else if (this.pinCode && this.pinCode.length > 0) {
        this.showError = false;
      }
    }
  },
  methods: {
    onClickOpenModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    handlePinCodeInput(number) {
      if (!this.pinCode) {
        this.pinCode = number;
      } else {
        this.pinCode += number;
      }
    },
    deleteInput() {
      if (this.pinCode.length > 0) {
        this.pinCode = this.pinCode.slice(0, -1);
      }
    }
  },
  computed: {
    emptyPinCode() {
      return !this.pinCode;
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

.user-name-button {
  width: 100%;
}
</style>
