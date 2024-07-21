<template>
  <main>
    <UserList />
  </main>
</template>
<script>
import UserList from '../components/users/UserList.vue';

export default {
  name: 'users-view',
  components: {
    UserList,
  }
};
</script>
