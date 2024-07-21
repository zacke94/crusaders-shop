<template>
  <div class="keypad-container">
    <Button class="keypad-item" label="1" @click="onClickKey(1)"></Button>
    <Button class="keypad-item" label="2" @click="onClickKey(2)"></Button>
    <Button class="keypad-item" label="3" @click="onClickKey(3)"></Button>
    <Button class="keypad-item" label="4" @click="onClickKey(4)"></Button>
    <Button class="keypad-item" label="5" @click="onClickKey(5)"></Button>
    <Button class="keypad-item" label="6" @click="onClickKey(6)"></Button>
    <Button class="keypad-item" label="7" @click="onClickKey(7)"></Button>
    <Button class="keypad-item" label="8" @click="onClickKey(8)"></Button>
    <Button class="keypad-item" label="9" @click="onClickKey(9)"></Button>
    <Button disabled class="keypad-item"></Button>
    <Button class="keypad-item" label="0" @click="onClickKey(0)"></Button>
    <Button disabled class="keypad-item"></Button>
  </div>
</template>

<script>
import Button from 'primevue/button';

export default {
  name: 'KeyPad',
  components: {
    Button
  },
  methods: {
    onClickKey(key) {
      this.$emit('handle-pin-code-input', key.toString());
    }
  }
};
</script>

<style scoped>
.keypad-container {
  display: flex;
  flex-wrap: wrap;
  width: 200px;
  height: 200px;
}

.keypad-item {
  flex: 0 0 33.33%;
  height: 32px;
  width: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
