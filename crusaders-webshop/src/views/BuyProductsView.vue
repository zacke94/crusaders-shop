<template>
  <Toast />
  <!-- TODO: change exclamation mark -->
  <div v-if="userIsAuthenticated(userId)">
    <Button label="Logga ut" @click="onClickLogout"></Button>
    <div class="buy-products-wrapper">
      <h1>Välj produkter</h1>

      <DataTable :value="products" tableStyle="min-width: 600px" class="products-table">
        <Column field="name" header="Produkt"></Column>
        <Column field="price" header="Pris">
          <template #body="slotProps">
            {{ slotProps.data.price }}
          </template>
        </Column>
        <!--      <Column header="Antal i lager">
        <template #body="slotProps">
          {{ slotProps.data.balance }}
          &lt;!&ndash;          <Tag :pinCode="slotProps.data.balance" :severity="getSeverity(slotProps.data)" />&ndash;&gt;
        </template>
      </Column>-->
        <Column field="quantity" header="Antal att köpa">
          <template #body="slotProps">
            <div class="quantity-wrapper">
              <Button
                label="-"
                @click="decreaseAmount(slotProps.data)"
                :disabled="slotProps.data.quantity === 0"
              ></Button>

              <p>{{ slotProps.data.quantity }}</p>

              <Button
                label="+"
                @click="increaseAmount(slotProps.data)"
                :disabled="slotProps.data.balance === 0"
              ></Button>
            </div>
          </template>
        </Column>

        <template #footer>
          <div class="table-footer">
            <h4 style="font-weight: bold">Totalbelopp: {{ totalAmount }} kr</h4>
            <ConfirmOrderModal :order="order" />
          </div>
        </template>
      </DataTable>
    </div>
  </div>
  <div v-else>
    <h1>Inte inloggad</h1>
  </div>
</template>

<script>
import { Product } from '@/models/Product';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ConfirmOrderModal from '@/components/modals/ConfirmOrderModal.vue';
import axios from 'axios';
import { Order } from '@/models/Order';
import router from '@/router';
import { storeMixin } from '@/mixins/store-mixin';
import store from '@/store';
import Toast from 'primevue/toast';

export default {
  name: 'buy-products-view',
  components: {
    ConfirmOrderModal,
    Button,
    DataTable,
    Column,
    Dialog,
    Toast
  },
  mixins: [storeMixin],
  props: {
    userId: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      products: [],
      orderProducts: [],
      order: null,
      totalAmount: 0
    };
  },
  methods: {
    decreaseAmount(product) {
      product.quantity--;

      this.orderProducts.find((p) => p.id === product.id).quantity--;
      this.changeAmount();
    },
    increaseAmount(product) {
      product.quantity++;

      if (!this.hasProductInOrder(product.id)) {
        const updatedOrder = new Product({
          ...product,
          balance: 0,
          quantity: 1
        });
        this.orderProducts.push(updatedOrder);
      } else {
        const item = this.orderProducts.find((p) => p.id === product.id);
        if (item) {
          item.quantity++;
          item.totalPrice = item.price * item.quantity;
        }
      }
      this.changeAmount();
    },
    hasProductInOrder(productId) {
      return this.orderProducts.some((product) => product.id === productId);
    },
    changeAmount() {
      let prices = 0;

      this.orderProducts.forEach((product) => {
        prices += product.price * product.quantity;
      });
      this.totalAmount = prices;
      this.updateOrder();
    },
    updateOrder() {
      this.order.totalPrice = this.totalAmount;
      this.order.products = this.orderProducts;
    },
    onClickLogout() {
      store.dispatch('logoutUser');
      router.push({ path: '/' });
    }
  },
  async created() {
    this.order = new Order({
      customerId: this.userId,
      totalPrice: 0
    });

    try {
      const response = await axios.get('http://127.0.0.1:5000/products');
      if (response.data.products.length > 0) {
        this.products = response.data.products.map(
          (product) =>
            new Product({
              id: product.id,
              name: product.name,
              price: product.price
            })
        );
      }
    } catch (error) {
      this.$toast.add({
        severity: 'error',
        summary: 'Något gick fel',
        detail: 'Skrik på Adam',
        life: 6000
      });
    }
  }
};
</script>

<style scoped>
.buy-products-wrapper {
  margin-top: 64px;
}

.products-table {
  margin-top: 32px;
  border: 1px solid gray;
  width: 100%;
}

.table-footer {
  display: flex;
  justify-content: space-between;
}

.quantity-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
