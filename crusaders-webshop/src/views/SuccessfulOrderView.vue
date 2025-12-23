<template>
  <div>
    <h1>Tack för ditt köp!</h1>
    <br />

    <h2>Tänk på att att vi kameraövervakar, och märker om ni INTE betalar</h2>

    <Button class="mt-32 center-div" label="Till startsidan" @click="onClickGoHome"></Button>
    <h3 class="mt-16">
      <span class="progress-bar-seconds"
        >Eller bli automatiskt omdirigeras till startsidan om {{ seconds }} sekunder...</span
      >
    </h3>
  </div>
</template>

<script>
import router from '@/router';
import Button from 'primevue/button';

export default {
  name: 'successful-order-view',
  components: {
    Button
  },
  data() {
    return {
      seconds: 5
    };
  },
  methods: {
    onClickGoHome() {
      router.replace({ path: '/' });
    }
  },
  mounted() {
    let timerId;

    /*if (this.seconds > 0) {
      timerId = setInterval(() => {
        this.seconds--;
        if (this.seconds <= 0) {
          clearInterval(timerId);
          router.replace({ path: '/' });
        }
      }, 1000);
    }*/
  }
};
</script>

<style scoped>
.center-div {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
