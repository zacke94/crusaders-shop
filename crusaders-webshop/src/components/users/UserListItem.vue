<template>
  <div>
    <Button :label="user.name" @click="openModal" />

    <Dialog v-model:visible="showModal" modal header="Logga in" :style="{ width: '25rem' }">
      <span class="p-text-secondary block mb-5">Skriv in din pinkod</span>
      <InputOtp v-model="pinCode" integerOnly />
    </Dialog>
  </div>
</template>

<script>
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import InputOtp from 'primevue/inputotp';
import axios from 'axios';
import { User } from '@/models/User'

export default {
  name: 'UserListItem',
  components: {
    Button,
    Dialog,
    InputOtp
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
      pinCode: null
    };
  },
  watch: {
    async pinCode() {
      if (this.pinCode.length === 4) {
        const passwordRequest = {
          userId: this.user.id,
          pinCode: this.pinCode
        }
        await axios.post('http://127.0.0.1:5000/login', passwordRequest);
        this.closeModal()
      }
    }
  },
  methods: {
    openModal() {
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    }
  }
};
</script>
