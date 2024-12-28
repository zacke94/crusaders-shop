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
import Button from 'primevue/button';
import ShowProductsModal from '@/components/modals/ShowProductsModal.vue';
import OrderService from '@/services/order-service';
import ToastService from '@/services/toast-service';

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
      this.orders = await OrderService.getOrder(parseInt(this.userId));
    } catch {
      ToastService.showError(this.$toast);
    }
  },
  methods: {
    onClickShowOrders() {
      this.showModal = true;
    }
  }
};
</script>
