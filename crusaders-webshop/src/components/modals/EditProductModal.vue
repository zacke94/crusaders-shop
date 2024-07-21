<template>
  <Toast />
  <Button label="Ändra produkt" @click="onClickEditProduct"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    :header="this.product.name"
    :style="{ width: '400px', height: '500px' }"
  >
    <div>
      <label for="name">Nytt namn</label>
      <InputText v-model="newProduct.name" type="text" inputId="name" maxlength="20" />
    </div>
    <div>
      <label for="price">Nytt pris</label>
      <InputText v-model="newProduct.price" type="text" inputId="price" maxlength="3" />
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

export default {
  name: 'EditProductModal',
  components: {
    Dialog,
    InputText,
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
      newProduct: new Product({ id: this.product.id })
    };
  },
  methods: {
    async onClickSave() {
      if (!this.newProduct.price && !this.newProduct.name) {
        return;
      }

      if (!this.newProduct.price) {
        this.newProduct.price = this.product.price;
      }
      if (!this.newProduct.name) {
        this.newProduct.name = this.product.name;
      }
      try {
        await axios.put('http://127.0.0.1:5000/edit-product', this.newProduct);
        this.$emit('updateProducts');

        this.newProduct.name = null;
        this.newProduct.price = null;
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
  }
};
</script>
