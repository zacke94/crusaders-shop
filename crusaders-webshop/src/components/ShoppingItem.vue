<template>
  <li>
    <h3>Antal tillgängliga: {{ totalAvailable }}</h3>
    <br />
    <h3>{{ name }} {{ price }} kr</h3>
    <br />
    <button
      @click="decrease"
      :disabled="nrOfItems === 0">
      -</button>
    <h3>Antal: {{ nrOfItems }}</h3>
    <button
      @click="increment"
      :disabled="itemsAreAvailable">
      +</button>
  </li>
</template>

<script>
export default {
  name: 'ShoppingItem',
  props: ['name', 'price', 'totalAvailable'],
  data() {
    return {
      nrOfItems: 0
    }
  },
  methods: {
    increment() {
      this.nrOfItems += 1;
    },
    decrease() {
      this.nrOfItems -= 1;
    }
  },
  computed: {
    itemsAreAvailable() {
      return this.nrOfItems >= 5 || this.nrOfItems === this.totalAvailable;
    }
  }
};
</script>
