<template>
  <Button
    icon="pi pi-pencil"
    size="small"
    severity="secondary"
    @click="onClickEditProduct"
  ></Button>
  <Dialog v-model:visible="showModal" modal :header="product.name">
    <div>
      <label for="name">Nytt namn</label>
      <InputText v-model="updatedProduct.name" type="text" inputId="name" maxlength="20" />
    </div>
    <div>
      <label for="price">Nytt pris</label>
      <InputNumber v-model="updatedProduct.price" inputId="price" maxlength="3" suffix=" kr" />
    </div>
    <div class="quantity-wrapper">
      <Button label="-" :disabled="disableDecreaseAmount" @click="decreaseAmount"></Button>
      <p>{{ updatedProduct.quantity }}</p>
      <Button label="+" @click="increaseAmount"></Button>
    </div>

    <Button label="Spara" class="mt-32" @click="onClickSave" />
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import { Product } from '@/models/Product';
import Button from 'primevue/button';
import cloneDeep from 'lodash/cloneDeep';
import InputText from 'primevue/inputtext';
import InputNumber from 'primevue/inputnumber';
import ProductService from '@/services/product-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'EditProductModal',
  components: {
    Dialog,
    Button,
    InputText,
    InputNumber
  },
  props: {
    product: {
      type: Product,
      required: true
    }
  },
  emits: ['updateProducts'],
  data() {
    return {
      showModal: false,
      updatedProduct: null
    };
  },
  computed: {
    disableDecreaseAmount() {
      return this.updatedProduct.quantity === 0;
    }
  },
  methods: {
    onClickEditProduct() {
      this.showModal = true;
    },
    increaseAmount() {
      this.updatedProduct.quantity++;
    },
    decreaseAmount() {
      if (!this.disableDecreaseAmount) {
        this.updatedProduct.quantity--;
      }
    },
    async onClickSave() {
      try {
        await ProductService.editProduct(this.updatedProduct);
        this.$emit('updateProducts');
        ToastService.showSuccess(this.$toast, `Uppdaterade '${this.product.name}'`);
        this.showModal = false;
      } catch {
        ToastService.showError(this.$toast);
      }
    }
  },
  mounted() {
    this.updatedProduct = cloneDeep(this.product);
  }
};
</script>

<style scoped>
.quantity-wrapper {
  display: flex;
  gap: 8px;
  align-items: center;
  margin-top: 16px;
}
</style>
