<template>
  <Toast />
  <div class="users-wrapper">
    <h1>Välj ditt namn i listan</h1>
    <UserListItem
      v-if="hasUsers"
      v-for="user in users"
      :key="user.id"
      :id="user.id"
      :user="user"
      class="user-list-item"
    />
    <div v-else class="mt-16">
      <p>Inga användare hittades.</p>
    </div>
  </div>
</template>

<script>
import UserListItem from './UserListItem.vue';
import Toast from 'primevue/toast';
import UserService from '@/services/user-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'UserList',
  components: {
    UserListItem,
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
      this.users = await UserService.getActiveUsers();
    } catch {
      ToastService.showError(this.$toast);
    }
  },
  computed: {
    hasUsers() {
      return this.users && this.users.length > 0;
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
