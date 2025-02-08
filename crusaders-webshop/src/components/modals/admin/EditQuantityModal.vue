<template>
  <Dialog
    v-model:visible="showModal"
    modal
    :header="this.product.name"
    :style="{ width: '400px', height: '500px' }"
  >
    <div>
      <label for="price">Nytt pris</label>
      <InputNumber v-model="updatedProduct.price" inputId="price" maxlength="3" suffix=" kr" />
      <KeyPad v-if="inputIsFocused" @handle-pin-code-input="handlePinCodeInput"></KeyPad>
    </div>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import { Product } from '@/models/Product';
import InputNumber from 'primevue/inputnumber';
import KeyPad from '@/components/KeyPad.vue';

export default {
  name: 'EditQuantityModal',
  components: {
    KeyPad,
    Dialog,
    InputNumber
  },
  props: {
    product: {
      type: Product,
      required: true
    }
  },
  data() {
    return {
      showModal: false,
      updatedProduct: null
    };
  },
  mounted() {
    this.updatedProduct = this.product;
  }
};
</script>
