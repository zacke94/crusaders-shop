<template>
  <Toast />
  <div class="users-wrapper">
    <h1>Välj ditt namn i listan</h1>
    <UserListItem
      v-for="user in users"
      :key="user.id"
      :id="user.id"
      :user="user"
      class="user-list-item"
    />
  </div>
</template>

<script>
import { User } from '@/models/User';
import Button from 'primevue/button';
import axios from 'axios';
import UserListItem from './UserListItem.vue';
import Dialog from 'primevue/dialog';
import InputOtp from 'primevue/inputotp';
import ScrollPanel from 'primevue/scrollpanel';
import Toast from 'primevue/toast';

export default {
  name: 'UserList',
  components: {
    UserListItem,
    Button,
    Dialog,
    InputOtp,
    ScrollPanel,
    Toast
  },
  data() {
    return {
      showModal: false,
      pinCode: null,
      users: []
    };
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/users');

      if (response.data.users.length > 0) {
        this.users = response.data.users.map((user) => new User(user));
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
};
</script>

<style scoped>
.users-wrapper {
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-list-item {
  padding: 16px 0;
}
</style>
