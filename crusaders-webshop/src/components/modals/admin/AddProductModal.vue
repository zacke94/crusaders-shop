<template>
  <Toast />
  <Button label="Lägg till produkt" @click="onClickAddProduct" class="mt-16"></Button>

  <Dialog
    v-model:visible="showModal"
    modal
    header="Lägg till produkt"
    :style="{ 'min-width': '400px', 'min-height': '200px' }"
  >
    <div class="card flex justify-content-center">
      <Button label="Spara" :disabled="disableSaveButton" @click="onClickSave"></Button>
    </div>
    <!--    <div>
      <div>
        <label for="name">Namn</label>
        <InputText v-model="newProduct.name" type="text" inputId="name" maxlength="20" />
      </div>
      <div>
        <label for="price">Pris</label>
        <InputText v-model="newProduct.price" type="number" inputId="price" maxlength="20" />
      </div>
    </div>-->
  </Dialog>
</template>

<script>
import Dialog from 'primevue/dialog';
import { Product } from '@/models/Product';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import axios from 'axios';
import Toast from 'primevue/toast';

export default {
  name: 'AddProductModal',
  components: {
    Dialog,
    InputText,
    Button,
    Toast
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
      return !this.newProduct.name || !this.newProduct.price;
    }
  },
  methods: {
    async onClickSave() {
      try {
        await axios.post('http://127.0.0.1:5000/add-product', this.newProduct);
        await this.$emit('updateProducts');
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
    onClickAddProduct() {
      this.showModal = true;
    }
  }
};
</script>
