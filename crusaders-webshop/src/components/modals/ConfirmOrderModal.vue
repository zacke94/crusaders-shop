<template>
  <Toast />
  <Button label="Köp" @click="onClickBuy" :disabled="order.totalPrice === 0"></Button>

  <Dialog :visible="showModal" modal :header="headerMessage" :style="{ 'min-width': '400px' }">
    <div v-if="!openingFridgeState" class="flex justify-content-end gap-2">
      <DataTable
        :value="order.products"
        :pt="{
          footer: {
            style: { 'margin-top': '32px' }
          }
        }"
      >
        <Column field="name" header="Produkt"></Column>
        <Column field="price" header="Pris/st"></Column>
        <Column field="quantity" header="Antal"></Column>
        <Column field="totalPrice" header="Summa"></Column>

        <template #footer>
          <p style="font-weight: bold">Totalbelopp: {{ order.totalPrice }} kr</p>
        </template>
      </DataTable>

      <div class="buttons">
        <Button type="button" label="Bekräfta köp" @click="onClickConfirmOrder"></Button>
        <Button
          type="button"
          label="Avbryt"
          severity="secondary"
          @click="onClickCloseModal"
        ></Button>
      </div>
    </div>

    <div v-else>
      <ProgressSpinner v-if="isLoading" />
      <div v-else>
        <span class="progress-bar-seconds"
          >Kylen låses automatiskt om {{ seconds }} sekunder...</span
        >
      </div>
    </div>
  </Dialog>
</template>

<script>
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import ProgressSpinner from 'primevue/progressspinner';
import router from '@/router';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import { Order } from '@/models/Order';
import axios from 'axios';
import store from '@/store';
import Toast from 'primevue/toast';

export default {
  name: 'ConfirmOrderModal',
  components: {
    Dialog,
    Button,
    ProgressSpinner,
    DataTable,
    Column,
    Toast
  },
  props: {
    order: {
      type: Order,
      required: true
    }
  },
  data() {
    return {
      openingFridgeState: false,
      showModal: false,
      isLoading: true,
      seconds: 10,
      headerMessage: 'Bekräfta köp'
    };
  },
  methods: {
    async unlockFridge() {
      this.openingFridgeState = true;
      this.headerMessage = 'Öppnar kylen....';

      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/unlock-fridge/${this.order.customerId}`,
          {
            isAdmin: false
          }
        );

        if (response.status === 200) {
          this.fridgeIsOpen();
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
        this.isLoading = false;
        this.openingFridgeState = false;
        this.onClickCloseModal();
      }
    },
    async onClickConfirmOrder() {
      this.isLoading = true;

      try {
        const response = await axios.post('http://127.0.0.1:5000/add-order', this.order);
        if (response.status === 200) {
          await this.unlockFridge();
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
      this.isLoading = false;
    },
    onClickCloseModal() {
      this.showModal = false;
    },
    fridgeIsOpen() {
      this.headerMessage = 'Kylen är öppen';
      this.isLoading = false;
      let timerId;

      if (this.seconds > 0) {
        timerId = setInterval(() => {
          this.seconds--;
          if (this.seconds <= 0) {
            clearInterval(timerId);
            this.closeFridge();
          }
        }, 1000);
      }
    },
    async closeFridge() {
      this.headerMessage = 'Kylen låses';
      this.isLoading = true;

      try {
        const response = await axios.post('http://127.0.0.1:5000/lock-fridge');
        if (response.status === 200) {
          this.onClickCloseModal();
          await router.push({ path: `/successful-order/${this.order.customerId}` });
          await store.dispatch('logoutUser', this.order.customerId);
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
      this.isLoading = false;
    },
    onClickBuy() {
      this.showModal = true;
    }
  }
};
</script>

<style scoped>
.buttons {
  display: flex;
  margin-top: 16px;
  gap: 8px;
}
</style>
