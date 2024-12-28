<template>
  <Toast />
  <Button label="Lägg till användare" @click="onClickAddUser" class="mt-16" />
  <Dialog v-model:visible="showModal" modal header="Lägg till användare">
    <div>
      <div>
        <label for="name">Användarnamn: </label>
        <InputText
          :invalid="invalidInput || isDuplicate"
          type="text"
          v-model="newUser.name"
          inputId="name"
          maxlength="15"
        />
        <span v-if="errorMessage">{{ errorMessage }}</span>
      </div>

      <div>
        <label for="pinCode">Pinkod</label>
        <InputText v-model="newUser.pinCode" type="password" inputId="pinCode" maxlength="4" />
      </div>

      <Button :disabled="disableAddUserButton" label="Lägg till" @click="addUser" />
    </div>

    <DataTable v-if="!emptyUsersList" :value="newUsers">
      <Column field="name"></Column>
      <Column>
        <template #body="slotProps">
          <Button label="Ta bort" severity="danger" @click="onClickRemoveUser(slotProps.data.id)" />
        </template>
      </Column>
    </DataTable>
    <Button label="Spara" :disabled="emptyUsersList" @click="onClickSave"></Button>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import { User } from '@/models/User';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputNumber from 'primevue/inputnumber';
import Toast from 'primevue/toast';
import UserService from '@/services/user-service';
import ToastService from '@/services/toast-service';

const validInput = '^[a-zA-ZäÄöÖåÅ]*$';

export default {
  name: 'AddUserModal',
  components: {
    Button,
    Dialog,
    InputText,
    DataTable,
    Column,
    InputNumber,
    Toast
  },
  props: {
    users: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  emits: ['updateUsers'],
  data() {
    return {
      showModal: false,
      newUser: new User(),
      newUsers: [],
      uniqueUserId: 0,
      errorMessage: '',
      maxlength: 4
    };
  },
  methods: {
    onClickAddUser() {
      this.showModal = true;
    },
    onClickRemoveUser(id) {
      this.newUsers = this.newUsers.filter((user) => user.id !== id);
    },
    async onClickSave() {
      try {
        await UserService.addUsers(this.newUsers);
        this.showModal = false;
        this.newUsers = [];
        this.$emit('updateUsers');
        ToastService.showSuccess(this.$toast, 'Användare har lagts till');
      } catch {
        ToastService.showError(this.$toast);
      }
    },
    addUser() {
      if (this.invalidInput || this.isDuplicate) return;
      const newUser = new User({
        id: this.uniqueUserId++,
        name: this.newUser.name,
        pinCode: parseInt(this.newUser.pinCode)
      });
      this.newUsers.push(newUser);
      this.newUser = new User();
    }
  },
  computed: {
    disableAddUserButton() {
      return (
        this.newUser.name.trim() === '' ||
        (this.newUser.pinCode && this.newUser.pinCode.length === 0)
      );
    },
    invalidInput() {
      const invalidInput = !this.newUser.name.match(validInput);

      if (invalidInput) {
        this.errorMessage = 'Ogiltiga tecken';
        return true;
      }
      this.errorMessage = '';
      return false;
    },
    emptyUsersList() {
      return this.newUsers.length === 0;
    },
    isDuplicate() {
      const isDuplicate =
        this.users.some((user) => user.name.toLowerCase() === this.newUser.name.toLowerCase()) ||
        this.newUsers.some((user) => user.name.toLowerCase() === this.newUser.name.toLowerCase());

      if (isDuplicate) {
        this.errorMessage = 'Användare finns redan';
        return true;
      }
      this.errorMessage = '';
      return false;
    }
  }
};
</script>
