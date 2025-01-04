<template>
  <Toast />
  <ConfirmDialog></ConfirmDialog>

  <div class="buttons-grid">
    <Button label="Tillbaka" @click="onClickGoBack"></Button>
    <Button label="Logga ut" @click="onClickLogout"></Button>
  </div>
  <div class="mt-32">
    <h1>Hantera ordrar</h1>

    <DataTable :value="orders" tableClass="mt-32">
      <template #empty v-if="emptyOrdersList"> Inga ordrar hittades. </template>
      <Column field="orderId" header="Order id"></Column>
      <Column field="orderDate" header="Order datum"></Column>
      <Column field="customerId" header="Kund id"></Column>
      <Column field="customerName" header="Kund namn"></Column>
      <Column>
        <template #body="slotProps">
          <div class="buttons-grid">
            <ShowProductsModal :order="slotProps.data" />
            <Button
              label="Radera"
              severity="danger"
              @click="onClickDeleteOrder(slotProps.data.orderId)"
            ></Button>
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Button from 'primevue/button';
import ShowProductsModal from '@/components/modals/ShowProductsModal.vue';
import Toast from 'primevue/toast';
import store from '@/store';
import router from '@/router';
import ConfirmDialog from 'primevue/confirmdialog';
import OrderService from '@/services/order-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'ManageOrdersView',
  components: {
    ShowProductsModal,
    DataTable,
    Column,
    Button,
    Toast,
    ConfirmDialog
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
    },
    async onClickLogout() {
      await store.dispatch('logoutAdmin');
      await router.push({ path: '/' });
    },
    async onClickDeleteOrder(orderId) {
      this.$confirm.require({
        message: 'Vill du ta ta väck ordern?',
        header: 'Varning',
        icon: 'pi pi-info-circle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Ja',
          severity: 'danger'
        },
        accept: async () => {
          try {
            await OrderService.deleteOrder(orderId);
            ToastService.showSuccess(this.$toast, 'Lyckades radera order');
            await this.getOrders();
          } catch {
            ToastService.showError(this.$toast);
          }
        }
      });
    },
    async getOrders() {
      try {
        this.orders = await OrderService.getOrders();
      } catch {
        ToastService.showError(this.$toast);
      }
    }
  },
  async mounted() {
    await this.getOrders();
  }
};
</script>
