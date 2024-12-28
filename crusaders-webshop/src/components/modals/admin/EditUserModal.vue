<template>
  <Toast />
  <Button label="Ändra pin" severity="secondary" @click="onClickEditPinCode"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    header="Ändra pinkod"
    :style="{ width: '400px', height: '500px' }"
  >
    <div>
      <label for="pinCode">Ny pinkod</label>
      <InputText v-model="user.pinCode" type="password" inputId="pinCode" maxlength="4" />
    </div>
    <div>
      <label for="confirmPinCode">Bekräfta ny pinkod</label>
      <InputText
        v-model="confirmedPinCode"
        type="password"
        inputId="confirmPinCode"
        maxlength="4"
      />
    </div>
    <Button label="Spara" @click="onClickSave"></Button>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import { User } from '@/models/User';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import UserService from '@/services/user-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'EditUserModal',
  components: {
    Dialog,
    InputText,
    Button,
    Toast
  },
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  emits: ['updateUsers'],
  data() {
    return {
      showModal: false,
      user: new User(),
      confirmedPinCode: ''
    };
  },
  methods: {
    async onClickSave() {
      try {
        await UserService.changePinCode({
          id: this.id,
          pinCode: parseInt(this.user.pinCode)
        });

        this.$emit('updateUsers');
        this.showModal = false;
        ToastService.showSuccess(this.$toast, 'Lyckades uppdatera pinkod');
      } catch {
        ToastService.showError(this.$toast);
      }
    },
    onClickEditPinCode() {
      this.showModal = true;
    }
  }
};
</script>
