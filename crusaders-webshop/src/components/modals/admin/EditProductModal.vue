<template>
  <Toast />
  <Button label="Ändra" severity="secondary" @click="onClickEditProduct"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    :header="this.product.name"
    :style="{ width: '400px', height: '500px' }"
  >
    <div>
      <label for="name">Nytt namn</label>
      <InputText v-model="updatedProduct.name" type="text" inputId="name" maxlength="20" />
    </div>
    <div>
      <label for="price">Nytt pris</label>
      <InputNumber v-model="updatedProduct.price" inputId="price" maxlength="3" suffix=" kr" />
    </div>
    <div>
      <label for="quantity">Saldo</label>
      <InputNumber v-model="updatedProduct.quantity" inputId="quantity" maxlength="2" />
    </div>
    <Button label="Spara" @click="onClickSave"></Button>
  </Dialog>
</template>

<script>
import { Product } from '@/models/Product';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import axios from 'axios';
import Toast from 'primevue/toast';
import InputNumber from 'primevue/inputnumber';

export default {
  name: 'EditProductModal',
  components: {
    Dialog,
    InputText,
    InputNumber,
    Button,
    Toast
  },
  emits: ['updateProducts'],
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
  methods: {
    async onClickSave() {
      try {
        await axios.put('http://127.0.0.1:5000/edit-product', this.updatedProduct);
        this.$emit('updateProducts');

        this.$toast.add({
          severity: 'success',
          summary: `Uppdaterade '${this.product.name}'`,
          life: 6000
        });
        this.showModal = false;
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
    },
    onClickEditProduct() {
      this.showModal = true;
    }
  },
  mounted() {
    this.updatedProduct = this.product;
  }
};
</script>
