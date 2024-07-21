<template>
  <div>
    <h1>Välj ditt namn i listan</h1>

    <div v-for="user in users" :key="user.id" :id="user.id">
      <UserListItem :user="user" />
    </div>
  </div>
</template>

<script>
import { User } from '../../models/User';
import Button from 'primevue/button';
import axios from 'axios';
import UserListItem from './UserListItem.vue';

export default {
  name: 'UserList',
  components: {
    UserListItem,
    Button
  },
  data() {
    return {
      users: []
    };
  },
  methods: {},
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/users');

      if (response.data.users.length > 0) {
        this.users = response.data.users.map((user) => new User(user));
      }
    } catch (e) {
      console.error(e);
    }
  }
};
</script>
