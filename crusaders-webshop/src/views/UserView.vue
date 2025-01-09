<template>
  <div class="card">
    <Toast />
    <div v-if="userIsAuthenticated(userId)">
      <div class="top-buttons">
        <Button label="Logga ut" @click="onClickLogout"></Button>
        <ShowOrdersModal :userId="userId" />
      </div>

      <div class="buy-products-wrapper">
        <h1>Hej {{ userName }}!</h1>

        <DataTable
          :value="products"
          tableStyle="min-width: 100%"
          class="products-table"
          :pt="{
            footer: {
              style: { 'margin-top': '32px' }
            }
          }"
        >
          <Column field="name" header="Produkt" style="width: 25%"></Column>
          <Column field="price" header="Pris" style="width: 25%">
            <template #body="slotProps">
              {{ slotProps.data.price }}
            </template>
          </Column>
          <Column header="Antal i lager">
            <template #body="slotProps">
              <Tag
                :icon="getQuantityIcon(slotProps.data.quantity)"
                :value="slotProps.data.quantity"
                :severity="getSeverity(slotProps.data.quantity)"
              />
            </template>
          </Column>
          <Column field="quantity" header="Antal att köpa" style="width: 25%">
            <template #body="slotProps">
              <div class="quantity-wrapper">
                <Button
                  label="-"
                  @click="decreaseAmount(slotProps.data)"
                  :disabled="disableDecreaseButton(slotProps.data)"
                ></Button>

                <p>{{ getAmountToBuy(slotProps.data) }}</p>

                <Button
                  label="+"
                  @click="increaseAmount(slotProps.data)"
                  :disabled="disableIncreaseButton(slotProps.data)"
                ></Button>
              </div>
            </template>
          </Column>

          <template #footer>
            <div class="table-footer">
              <h4 class="bold-text">Totalbelopp: {{ totalAmount }} kr</h4>
              <ConfirmOrderModal :order="order" />
            </div>
          </template>
        </DataTable>
      </div>
    </div>
    <div v-else>
      <h1>Inte inloggad</h1>
      <Button label="Gå till startsida" class="mt-32" @click="onClickGoHome"></Button>
    </div>
  </div>
</template>

<script>
import { Product } from '@/models/Product';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ConfirmOrderModal from '@/components/modals/ConfirmOrderModal.vue';
import { Order } from '@/models/Order';
import router from '@/router';
import { storeMixin } from '@/mixins/store-mixin';
import store from '@/store';
import Toast from 'primevue/toast';
import ShowOrdersModal from '@/components/modals/ShowOrdersModal.vue';
import { Tag } from 'primevue';
import UserService from '@/services/user-service';
import ToastService from '@/services/toast-service';
import ProductService from '@/services/product-service';

export default {
  name: 'UserView',
  components: {
    ShowOrdersModal,
    ConfirmOrderModal,
    Button,
    DataTable,
    Column,
    Dialog,
    Toast,
    Tag
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
      totalAmount: 0,
      user: null
    };
  },
  methods: {
    decreaseAmount(product) {
      if (this.hasProductInOrder(product.id)) {
        this.orderProducts.find((p) => p.id === product.id).quantity--;
        this.changeAmount();
      }
    },
    increaseAmount(product) {
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
    async onClickLogout() {
      await store.dispatch('logoutUser');
      await router.push({ path: '/' });
    },
    async onClickGoHome() {
      await router.push({ path: '/' });
    },
    getQuantityIcon(quantity) {
      return quantity > 0 ? 'pi pi-check' : 'pi pi-times';
    },
    getSeverity(quantity) {
      return quantity > 0 ? 'success' : 'danger';
    },
    getAmountToBuy(product) {
      return this.orderProducts.find((p) => p.id === product.id)?.quantity || 0;
    },
    disableDecreaseButton(product) {
      if (product.quantity === 0) {
        return true;
      }
      const productInOrder = this.orderProducts.find((p) => p.id === product.id);
      return productInOrder ? productInOrder.quantity === 0 : true;
    },
    disableIncreaseButton(product) {
      if (product.quantity === 0) {
        return true;
      }
      const productInOrder = this.orderProducts.find((p) => p.id === product.id);
      return productInOrder ? productInOrder.quantity === product.quantity : false;
    }
  },
  computed: {
    userName() {
      return this.user?.name;
    }
  },
  async created() {
    this.order = new Order({
      customerId: this.userId,
      totalPrice: 0
    });

    try {
      this.user = await UserService.getUser(parseInt(this.userId));
      this.products = await ProductService.getEligibleProducts();
    } catch {
      ToastService.showError(this.$toast);
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

.table-footer,
.top-buttons {
  display: flex;
  justify-content: space-between;
}

.quantity-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
}
</style>
