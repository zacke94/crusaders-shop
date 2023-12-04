<template>
  <ShoppingCart></ShoppingCart>
</template>

<script>
import ShoppingCart from '../components/ShoppingCart.vue'

export default {
  name: 'ShopView',
  components: { ShoppingCart },
  inject: ['shoppingItems']
};
</script>
