<template>
  <Button label="Produkter" @click="onClickShowProducts"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    header="Visa produkter"
    :style="{ width: '600px', height: '500px' }"
  >
    <DataTable :value="order.products">
      <Column field="productId" header="Produkt id"></Column>
      <Column field="productName" header="Produkt namn"></Column>
      <Column field="quantity" header="Antal"></Column>
      <Column field="totalPrice" header="Summa pris"></Column>
    </DataTable>
    <br />
    <p class="bold-text">Totala beloppet: {{ order.totalPrice }} kr</p>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { Order } from '@/models/Order';
import Button from 'primevue/button';

export default {
  name: 'ShowProductsModal',
  components: {
    Dialog,
    Button,
    DataTable,
    Column
  },
  props: {
    order: {
      type: Order,
      required: true
    }
  },
  data() {
    return {
      showModal: false
    };
  },
  methods: {
    onClickShowProducts() {
      this.showModal = true;
    }
  }
};
</script>
