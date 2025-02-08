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

    <DataTable v-if="!emptyProductsList" :value="products" tableClass="mt-16">
      <Column field="name" header="Namn">
        <template #body="slotProps">
          <div class="buttons-grid">
            <p>{{ slotProps.data.name }} kr</p>
            <Button icon="pi pi-pencil" size="small" severity="secondary"></Button>
          </div>
        </template>
      </Column>
      <Column field="price" header="Pris">
        <template #body="slotProps">
          <div class="buttons-grid">
            <p>{{ slotProps.data.price }} kr</p>
            <Button icon="pi pi-pencil" size="small" severity="secondary"></Button>
          </div>
        </template>
      </Column>
      <Column field="quantity" header="Saldo">
        <template #body="slotProps">
          <div class="buttons-grid">
            <p>{{ slotProps.data.quantity }}</p>
            <Button icon="pi pi-pencil" size="small" severity="secondary"></Button>
          </div>
        </template>
      </Column>
      <Column header="Dold">
        <template #body="slotProps">
          <p>{{ showProduct(slotProps.data.showProduct) }}</p>
        </template>
      </Column>
      <Column>
        <template #body="slotProps">
          <!--            <EditProductModal :product="slotProps.data" @update-products="handleUpdateProducts" />-->
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
import ConfirmPopup from 'primevue/confirmpopup';
import EditProductModal from '@/components/modals/admin/EditProductModal.vue';
import AddProductModal from '@/components/modals/admin/AddProductModal.vue';
import Toast from 'primevue/toast';
import store from '@/store';
import router from '@/router';
import ProductService from '@/services/product-service';
import ToastService from '@/services/toast-service';

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
            await ProductService.hideProduct(product.id);
            await this.getProducts();
            ToastService.showSuccess(this.$toast, `${product.name} är nu dold`);
          } catch {
            ToastService.showError(this.$toast);
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
            await ProductService.showProduct(product.id);
            await this.getProducts();
            ToastService.showSuccess(this.$toast, `${product.name} är nu synlig.`);
          } catch {
            ToastService.showError(this.$toast);
          }
        }
      });
    },
    async handleUpdateProducts() {
      await this.getProducts();
    },
    async getProducts() {
      try {
        this.products = await ProductService.getAllProducts();
      } catch {
        ToastService.showError(this.$toast);
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
