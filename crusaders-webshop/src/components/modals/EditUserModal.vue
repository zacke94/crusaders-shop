<template>
  <Toast />
  <Button label="Ändra pin" @click="onClickEditPinCode"></Button>

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
import axios from 'axios';
import Toast from 'primevue/toast';

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
        await axios.put('http://127.0.0.1:5000/change-pin-code', {
          id: this.id,
          pinCode: parseInt(this.user.pinCode)
        });
        this.$emit('updateUsers');
        this.showModal = false;
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
    },
    onClickEditPinCode() {
      this.showModal = true;
    }
  }
};
</script>
