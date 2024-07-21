<template>
  <Button label="Tidigare ordrar" @click="onClickShowOrders"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    header="Tidigare ordrar"
    :style="{ width: '600px', height: '500px' }"
  >
    <DataTable
      v-model:expandedRows="expandedRows"
      :value="orders"
      dataKey="orderId"
      scrollable
      scrollHeight="400px"
      :pt="{ thead: { style: { 'background-color': 'red' } } }"
    >
      <Column expander style="width: 5rem" />
      <Column field="orderId" header="Order id"></Column>
      <Column field="orderDate" header="Order datum"></Column>

      <template #expansion="slotProps">
        <div class="p-4">
          <DataTable :value="slotProps.data.products">
            <Column field="productId" header="Produkt id"></Column>
            <Column field="productName" header="Produkt namn"></Column>
            <Column field="quantity" header="Antal"></Column>
            <Column field="totalPrice" header="Summa pris"></Column>
          </DataTable>
          <br />
          <p class="bold-text">Totala beloppet: {{ slotProps.data.totalPrice }} kr</p>
        </div>
      </template>
    </DataTable>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { Order } from '@/models/Order';
import Button from 'primevue/button';
import axios from 'axios';
import ShowProductsModal from '@/components/modals/ShowProductsModal.vue';

export default {
  name: 'ShowOrdersModal',
  components: {
    ShowProductsModal,
    Dialog,
    Button,
    DataTable,
    Column
  },
  props: {
    userId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showModal: false,
      orders: [],
      expandedRows: {}
    };
  },
  async created() {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/get-order/${this.userId}`);
      if (response.data.length > 0) {
        this.orders = response.data.map((order) => new Order(order));
      }
    } catch (error) {
      this.$toast.add({
        severity: 'error',
        summary: 'Något gick fel',
        detail: 'Skrik på Adam',
        life: 6000
      });
    }
  },
  methods: {
    onClickShowOrders() {
      this.showModal = true;
    }
  }
};
</script>
