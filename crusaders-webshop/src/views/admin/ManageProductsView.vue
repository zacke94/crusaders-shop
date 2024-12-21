<template>
  <Toast />
  <div class="buttons-grid">
    <Button label="Tillbaka" @click="onClickGoBack"></Button>
    <Button label="Logga ut" @click="onClickLogout"></Button>
  </div>

  <div class="mt-32">
    <h1>Hantera produkter</h1>

    <AddProductModal @update-products="handleUpdateProducts" />
    <ConfirmPopup></ConfirmPopup>

    <DataTable v-if="!emptyProductsList" scrollable :value="products" tableClass="mt-16">
      <Column field="name" header="Namn"></Column>
      <Column field="price" header="Pris"></Column>
      <Column field="quantity" header="Saldo"></Column>
      <Column header="Dold">
        <template #body="slotProps">
          <p>{{ showProduct(slotProps.data.showProduct) }}</p>
        </template>
      </Column>
      <Column>
        <template #body="slotProps">
          <div class="buttons-grid">
            <EditProductModal :product="slotProps.data" @update-products="handleUpdateProducts" />
            <Button
              v-if="slotProps.data.showProduct"
              label="Dölj"
              severity="danger"
              @click="onClickHideProduct($event, slotProps.data)"
            ></Button>
            <Button
              v-else
              label="Visa"
              severity="success"
              @click="onClickShowProduct($event, slotProps.data)"
            ></Button>
          </div>
        </template>
      </Column>
    </DataTable>
  </div>
</template>

<script>
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ConfirmDialog from 'primevue/confirmdialog';
import axios from 'axios';
import { Product } from '@/models/Product';
import ConfirmPopup from 'primevue/confirmpopup';
import EditProductModal from '@/components/modals/admin/EditProductModal.vue';
import AddProductModal from '@/components/modals/admin/AddProductModal.vue';
import Toast from 'primevue/toast';
import store from '@/store';
import router from '@/router';

export default {
  name: 'ManageProductsView',
  components: {
    EditProductModal,
    AddProductModal,
    Button,
    DataTable,
    Column,
    ConfirmDialog,
    ConfirmPopup,
    Toast
  },
  data() {
    return {
      id: null,
      products: [],
      product: null
    };
  },
  methods: {
    async onClickHideProduct(event, product) {
      this.$confirm.require({
        target: event.currentTarget,
        message: `Är du säker att du vill dölja ${product.name}?`,
        icon: 'pi pi-exclamation-triangle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Ja'
        },
        accept: async () => {
          try {
            const response = await axios.put(`http://127.0.0.1:5000/hide-product/${product.id}`);
            if (response.status === 200) {
              await this.getProducts();
              this.$toast.add({
                severity: 'success',
                summary: `Lyckades ta dölja ${product.name}`,
                life: 3000
              });
            }
          } catch (e) {
            this.$toast.add({
              severity: 'error',
              summary: 'Något gick fel',
              detail: 'Skrik på Adam',
              life: 6000
            });
          }
        }
      });
    },
    async onClickShowProduct(event, product) {
      this.$confirm.require({
        target: event.currentTarget,
        message: `Är du säker att du vill visa ${product.name}?`,
        icon: 'pi pi-exclamation-triangle',
        rejectProps: {
          label: 'Avbryt',
          severity: 'secondary',
          outlined: true
        },
        acceptProps: {
          label: 'Ja'
        },
        accept: async () => {
          try {
            const response = await axios.put(`http://127.0.0.1:5000/show-product/${product.id}`);
            if (response.status === 200) {
              await this.getProducts();
              this.$toast.add({
                severity: 'success',
                summary: `Lyckades ta visa ${product.name}`,
                life: 3000
              });
            }
          } catch (e) {
            this.$toast.add({
              severity: 'error',
              summary: 'Något gick fel',
              detail: 'Skrik på Adam',
              life: 6000
            });
          }
        }
      });
    },
    async handleUpdateProducts() {
      await this.getProducts();
    },
    async getProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/all-products');
        if (response.data.products.length > 0) {
          this.products = response.data.products.map(
            (product) =>
              new Product({
                id: product.id,
                name: product.name,
                price: product.price,
                quantity: product.quantity,
                showProduct: product.showProduct
              })
          );
        }
      } catch (e) {
        this.$toast.add({
          severity: 'error',
          summary: 'Något gick fel',
          detail: 'Skrik på Adam',
          life: 6000
        });
      }
    },
    async onClickGoBack() {
      await this.$router.back();
    },
    showProduct(showProduct) {
      return showProduct ? 'Nej' : 'Ja';
    },
    async onClickLogout() {
      await store.dispatch('logoutAdmin');
      await router.push({ path: '/' });
    }
  },
  computed: {
    emptyProductsList() {
      return this.products && this.products.length === 0;
    }
  },
  async mounted() {
    await this.getProducts();
  }
};
</script>
