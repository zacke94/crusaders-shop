<template>
  <div class="buttons-grid">
    <Button label="Tillbaka" @click="onClickGoBack"></Button>
    <Button label="Logga ut" @click="onClickLogout"></Button>
  </div>

  <Toast />
  <div class="mt-32">
    <h1>Hantera användare</h1>

    <AddUserModal :users="users" @update-users="handleUpdateUsers" />
    <ConfirmDialog></ConfirmDialog>

    <DataTable v-if="!emptyUsersList" :value="users" tableClass="mt-16">
      <Column field="name" header="Namn"></Column>
      <Column header="Aktiv">
        <template #body="slotProps">
          <p>{{ isActive(slotProps.data) }}</p>
        </template>
      </Column>
      <Column>
        <template #body="slotProps">
          <div class="buttons-grid">
            <EditUserModal :id="slotProps.data.id" @update-users="handleUpdateUsers" />
            <Button
              v-if="slotProps.data.isActive"
              label="Inaktivera"
              severity="danger"
              @click="onClickInactivateUser(slotProps.data)"
            ></Button>
            <Button
              v-else
              label="Aktivera"
              severity="success"
              @click="onClickActivateUser(slotProps.data)"
            ></Button>
          </div>
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
import Toast from 'primevue/toast';
import store from '@/store';
import router from '@/router';

export default {
  name: 'ManageUsersView',
  components: {
    AddUserModal,
    EditUserModal,
    Button,
    DataTable,
    Column,
    ConfirmDialog,
    Toast
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
    async onClickInactivateUser(user) {
      this.$confirm.require({
        message: `Vill du ta inaktivera ${user.name}?`,
        header: 'Varning',
        icon: 'pi pi-info-circle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Ja',
          severity: 'danger'
        },
        accept: async () => {
          try {
            await axios.put(`http://127.0.0.1:5000/inactivate-user/${user.id}`);
            this.$toast.add({
              severity: 'success',
              summary: `Lyckades inaktivera ${user.name}`,
              life: 3000
            });
            await this.getUsers();
          } catch (e) {
            this.$toast.add({
              severity: 'error',
              summary: 'Något gick fel',
              detail: 'Skrik på Adam',
              life: 6000
            });
          }
        }
      });
    },
    async onClickActivateUser(user) {
      this.$confirm.require({
        message: `Vill du ta aktivera ${user.name}?`,
        header: 'Varning',
        icon: 'pi pi-info-circle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Ja',
          severity: 'danger'
        },
        accept: async () => {
          try {
            await axios.put(`http://127.0.0.1:5000/activate-user/${user.id}`);
            this.$toast.add({
              severity: 'success',
              summary: `Lyckades aktivera ${user.name}`,
              life: 3000
            });
            await this.getUsers();
          } catch (e) {
            this.$toast.add({
              severity: 'error',
              summary: 'Något gick fel',
              detail: 'Skrik på Adam',
              life: 6000
            });
          }
        }
      });
    },
    async getUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/all-users');
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
    },
    async handleUpdateUsers() {
      await this.getUsers();
    },
    async onClickGoBack() {
      await this.$router.back();
    },
    async onClickLogout() {
      await store.dispatch('logoutAdmin');
      await router.push({ path: '/' });
    },
    isActive(user) {
      return user.isActive ? 'Ja' : 'Nej';
    }
  },
  async mounted() {
    await this.getUsers();
  }
};
</script>
