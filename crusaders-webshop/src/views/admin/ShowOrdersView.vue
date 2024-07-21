<template>
  <Button label="Tillbaka" @click="onClickGoBack"></Button>

  <div class="mt-32">
    <h1>Visa ordrar</h1>

    <DataTable v-if="!emptyOrdersList" :value="orders" tableClass="mt-32">
      <Column field="orderId" header="Order id"></Column>
      <Column field="orderDate" header="Order datum"></Column>
      <Column field="customerId" header="Kund id"></Column>
      <Column field="customerName" header="Kund namn"></Column>
      <Column>
        <template #body="slotProps">
          <ShowProductsModal :order="slotProps.data" />
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import axios from 'axios';
import { Order } from '@/models/Order';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import ShowProductsModal from '@/components/modals/ShowProductsModal.vue';

export default {
  name: 'ShowOrdersView',
  components: {
    ShowProductsModal,
    DataTable,
    Column,
    Button
  },
  data() {
    return {
      orders: [],
      showModal: false,
      productsToShow: [],
      totalOrderPrice: 0
    };
  },
  computed: {
    emptyOrdersList() {
      return this.orders.length === 0;
    }
  },
  methods: {
    async onClickGoBack() {
      await this.$router.back();
    }
  },
  async mounted() {
    try {
      const response = await axios.get('http://127.0.0.1:5000/get-orders');
      if (response.data.length > 0) {
        this.orders = response.data.map((order) => new Order(order));
      }
    } catch (e) {
      console.log(e);
    }
  }
};
</script>
