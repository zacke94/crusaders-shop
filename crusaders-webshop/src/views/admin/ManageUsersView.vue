<template>
  <Button label="Tillbaka" @click="onClickGoBack"></Button>

  <div class="mt-32">
    <h1>Hantera användare</h1>

    <AddUserModal :users="users" @update-users="handleUpdateUsers" />
    <ConfirmDialog></ConfirmDialog>

    <DataTable v-if="!emptyUsersList" :value="users" tableClass="mt-16">
      <Column field="name" header="Namn"></Column>
      <Column>
        <template #body="slotProps">
          <EditUserModal :id="slotProps.data.id" @update-users="handleUpdateUsers" />
          <Button
            label="Ta bort"
            severity="danger"
            @click="onClickRemoveUser(slotProps.data)"
          ></Button>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import AddUserModal from '@/components/modals/admin/AddUserModal.vue';
import EditUserModal from '@/components/modals/admin/EditUserModal.vue';
import axios from 'axios';
import { User } from '@/models/User';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ConfirmDialog from 'primevue/confirmdialog';

export default {
  name: 'ManageUsersView',
  components: {
    AddUserModal,
    EditUserModal,
    Button,
    DataTable,
    Column,
    ConfirmDialog
  },
  data() {
    return {
      users: [],
      id: null,
      showEditPinCodeModal: false
    };
  },
  computed: {
    emptyUsersList() {
      return this.users.length === 0;
    }
  },
  methods: {
    async onClickRemoveUser(user) {
      this.$confirm.require({
        message: `Vill du ta väck ${user.name}?`,
        header: 'Varning',
        icon: 'pi pi-info-circle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Radera',
          severity: 'danger'
        },
        accept: async () => {
          await axios.delete('http://127.0.0.1:5000/delete-user', { data: { id: user.id } });
          await this.getUsers();
          this.$toast.add({
            severity: 'success',
            summary: `Lyckades ta väck ${user.name}`,
            life: 3000
          });
        },
        reject: () => {}
      });
    },
    async getUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/users');
        if (response.data.users.length > 0) {
          this.users = response.data.users.map((user) => new User(user));
        }
      } catch (e) {
        console.log(e);
      }
    },
    async handleUpdateUsers() {
      await this.getUsers();
    },
    async onClickGoBack() {
      await this.$router.back();
    }
  },
  async mounted() {
    await this.getUsers();
  }
};
</script>
