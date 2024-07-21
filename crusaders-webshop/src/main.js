import './assets/main.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';
import store from './store';
import ConfirmationService from 'primevue/confirmationservice';
import { definePreset } from '@primevue/themes';
import ToastService from 'primevue/toastservice';

import PrimeVue from 'primevue/config';

const app = createApp(App);

app.use(router);
app.use(store);
app.use(ToastService);
app.use(PrimeVue, {
  theme: {
    preset: definePreset(Aura)
  }
});
app.use(ConfirmationService);

app.mount('#app');
