<template>
  <div class="card">
    <h1>Välj produkter</h1>

    <DataTable :value="products" scrollable scrollHeight="400px" tableStyle="min-width: 50rem">
      <template #header>
        <div class="flex flex-wrap align-items-center justify-content-between gap-2">
          <span class="text-xl text-900 font-bold">Produkter</span>
        </div>
      </template>

      <Column field="name" header="Produkt"></Column>

      <Column field="price" header="Pris">
        <template #body="slotProps">
          {{ slotProps.data.price }}
        </template>
      </Column>

      <Column header="Antal i lager">
        <template #body="slotProps">
          {{ slotProps.data.balance }}
          <!--          <Tag :pinCode="slotProps.data.balance" :severity="getSeverity(slotProps.data)" />-->
        </template>
      </Column>

      <Column field="quantity" header="Antal att köpa">
        <template #body="slotProps">
          <Button
            label="-"
            @click="decreaseAmount(slotProps.data)"
            :disabled="slotProps.data.quantity === 0"
          ></Button>

          {{ slotProps.data.quantity }}

          <Button
            label="+"
            @click="increaseAmount(slotProps.data)"
            :disabled="slotProps.data.balance === 0"
          ></Button>
        </template>
      </Column>
      <template #footer> Totalbelopp: {{ totalAmount }} kr </template>
    </DataTable>

    <Button label="Köp" @click="openConfirmModal" :disabled="totalAmount === 0"></Button>

    <Dialog
      :visible="showConfirmModal"
      modal
      header="Bekräfta ditt köp"
      :style="{ width: '25rem' }"
    >
      <div class="flex justify-content-end gap-2">
        <Button type="button" label="Bekräfta köp" @click="openFridgeModal"></Button>
        <Button
          type="button"
          label="Avbryt"
          severity="secondary"
          @click="closeConfirmModal"
        ></Button>
      </div>
      <!--      <span class="p-text-secondary block mb-5">Update your information.</span>
      <div class="flex align-items-center gap-3 mb-3">
        <label for="username" class="font-semibold w-6rem">Username</label>
        &lt;!&ndash;        <InputText id="username" class="flex-auto" autocomplete="off" />&ndash;&gt;
      </div>
      <div class="flex align-items-center gap-3 mb-5">
        <label for="email" class="font-semibold w-6rem">Email</label>
        &lt;!&ndash;        <InputText id="Email" class="flex-auto" autocomplete="off" />&ndash;&gt;
      </div>
      <div class="flex justify-content-end gap-2">
        <Button type="button" label="Cancel" severity="secondary" @click="closeConfirmModal"></Button>
        <Button type="button" label="Save" @click="closeConfirmModal"></Button>
      </div>-->
    </Dialog>

    <Dialog :visible="showFridgeModal" modal header="Öppnar kyl.." :style="{ width: '25rem' }">
      <span class="progress-bar-seconds">{{ seconds }} Seconds left ...</span>
      <Button type="button" label="Stäng" severity="secondary" @click="closeFridgeModal"></Button>
    </Dialog>
  </div>
</template>

<script>
import { Product } from '../models/Product';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

export default {
  name: 'buy-products-view',
  components: {
    Button,
    DataTable,
    Column,
    Dialog
  },
  props: {
    userId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      products: [new Product(1, 10, 'Cola vanlig', 15, 0), new Product(2, 7, 'Nocco', 25, 0)],
      buyOrder: [],
      totalAmount: 0,
      showConfirmModal: false,
      showFridgeModal: false,
      seconds: 5
    };
  },
  methods: {
    decreaseAmount(product) {
      product.quantity--;

      this.buyOrder.find((p) => p.id === product.id).quantity--;
      this.changeAmount();
    },
    increaseAmount(product) {
      product.quantity++;

      if (!this.hasProductInOrder(product.id)) {
        this.buyOrder.push({ ...product, balance: 0, quantity: 1 });
      } else {
        this.buyOrder.find((p) => p.id === product.id).quantity++;
      }
      this.changeAmount();
    },
    hasProductInOrder(productId) {
      return this.buyOrder.some((product) => product.id === productId);
    },
    changeAmount() {
      let prices = 0;

      this.buyOrder.forEach((product) => {
        prices += product.price * product.quantity;
      });
      this.totalAmount = prices;
    },
    openConfirmModal() {
      this.showConfirmModal = true;
    },
    closeConfirmModal() {
      this.showConfirmModal = false;
    },
    openFridgeModal() {
      this.closeConfirmModal();
      this.showFridgeModal = true;
      let timerId;

      if (this.seconds > 0) {
        timerId = setInterval(() => {
          this.seconds--;
          if (this.seconds <= 0) {
            clearInterval(timerId);
            this.closeFridgeModal();
          }
        }, 1000);
      }
    },

    closeFridgeModal() {
      this.showFridgeModal = false;
    }
    /* link() {
      return `/buy-products/${this.userId}/confirm-order/`;
    }*/
  }
};
</script>
