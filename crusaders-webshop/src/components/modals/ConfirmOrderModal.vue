<template>
  <Toast />
  <Button label="Köp" @click="onClickBuy" :disabled="order.totalPrice === 0"></Button>

  <Dialog
    :visible="showModal"
    modal
    :header="headerMessage"
    :style="{ 'min-width': '400px' }"
    :closable="!openingFridgeState"
  >
    <div v-if="!openingFridgeState">
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
          <p class="bold-text">Totalbelopp: {{ order.totalPrice }} kr</p>
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
        <p>
          Totalbelopp: <span class="bold-text">{{ order.totalPrice }} kr</span>
        </p>
        <p>Swish: <span class="bold-text">123-651 60 33</span></p>
        <p class="mt-16">
          Kylen låses automatiskt om
          <span class="progress-bar-seconds bold-text">{{ seconds }} sekunder...</span>
        </p>
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
import store from '@/store';
import Toast from 'primevue/toast';
import FridgeService from '@/services/fridge-service';
import ToastService from '@/services/toast-service';
import OrderService from '@/services/order-service';

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
      seconds: 30,
      headerMessage: 'Bekräfta köp'
    };
  },
  methods: {
    async unlockFridge(orderId) {
      this.openingFridgeState = true;
      this.headerMessage = 'Öppnar kylen....';

      try {
        const requestData = {
          isAdmin: false,
          customerId: this.order.customerId,
          orderId: orderId
        };
        await FridgeService.unlockFridge(requestData);
        this.fridgeIsOpen();
      } catch {
        ToastService.showError(this.$toast);
        this.isLoading = false;
        this.openingFridgeState = false;
        this.onClickCloseModal();
      }
    },
    async onClickConfirmOrder() {
      this.isLoading = true;

      try {
        const orderId = await OrderService.addOrder(this.order);
        await this.unlockFridge(orderId);
      } catch {
        ToastService.showError(this.$toast);
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
        await FridgeService.lockFridge();
        this.onClickCloseModal();
        await router.push({ path: `/successful-order/${this.order.customerId}` });
        await store.dispatch('logoutUser', this.order.customerId);
      } catch {
        ToastService.showError(this.$toast);
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
