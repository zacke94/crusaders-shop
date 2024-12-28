<template>
  <Toast />
  <Button label="Lägg till produkt" @click="onClickAddProduct" class="mt-16"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    header="Lägg till produkt"
    :style="{ 'min-width': '400px', 'min-height': '200px' }"
  >
    <div>
      <div>
        <label for="name">Namn</label>
        <InputText v-model="newProduct.name" type="text" inputId="name" maxlength="20" />
      </div>
      <div>
        <label for="price">Pris</label>
        <InputText v-model="newProduct.price" type="number" inputId="price" maxlength="20" />
      </div>
    </div>

    <div class="card flex justify-content-center">
      <Button label="Spara" :disabled="disableSaveButton" @click="onClickSave"></Button>
    </div>
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import { Product } from '@/models/Product';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Toast from 'primevue/toast';
import { Form, FormField } from '@primevue/forms';
import Message from 'primevue/message';
import ProductService from '@/services/product-service';
import ToastService from '@/services/toast-service';

export default {
  name: 'AddProductModal',
  components: {
    Dialog,
    InputText,
    Button,
    Toast,
    Form,
    FormField,
    Message
  },
  emits: ['updateProducts'],
  data() {
    return {
      showModal: false,
      newProduct: new Product()
    };
  },
  computed: {
    disableSaveButton() {
      return !this.newProduct.name && !this.newProduct.price;
    }
  },
  methods: {
    async onClickSave() {
      try {
        await ProductService.addProduct(this.newProduct);
        await this.$emit('updateProducts');
        this.showModal = false;
        this.product = new Product();
      } catch {
        ToastService.showError(this.$toast);
      }
    },
    onClickAddProduct() {
      this.showModal = true;
    }
  }
};
</script>
