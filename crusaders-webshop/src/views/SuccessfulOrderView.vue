<template>
  <div>
    <h1>Tack för ditt köp!</h1>

    <h3>Tänk på att att vi kameraövervakar, och märker om ni INTE betalar</h3>
    <br />

    <span class="progress-bar-seconds"
      >Du blir omdirigeras till startsidan om {{ seconds }} sekunder...</span
    >
  </div>
</template>

<script>
import router from '@/router';

export default {
  name: 'successful-order-view',
  data() {
    return {
      seconds: 10
    };
  },
  mounted() {
    let timerId;

    if (this.seconds > 0) {
      timerId = setInterval(() => {
        this.seconds--;
        if (this.seconds <= 0) {
          clearInterval(timerId);
          router.replace({ path: '/' });
        }
      }, 1000);
    }
  }
};
</script>
