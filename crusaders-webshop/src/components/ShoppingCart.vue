<template>
  <ul>
    <ShoppingItem
      v-for="item in shoppingItems"
      :key="item.id"
      :id="item.id"
      :name="item.name"
      :price="item.price"
      :totalAvailable="item.totalAvailable"
    ></ShoppingItem>
  </ul>
</template>

<script>
export default {
  props: ['shoppingItems'],
};
</script>
