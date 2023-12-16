<template>
  <div v-if="connected">
    <p>Connected</p>
    <button v-if="locked" @click="unlockDevice">Unlock device</button>
    <button v-else @click="lockDevice">Lock device</button>
  </div>
  <p v-else>Not connected</p>
  <p v-if="errorMsg" color="red">{{ errorMsg }}</p>
</template>

<script>
import axios from 'axios';

export default {
  name: 'device',
  data() {
    return {
      connected: false,
      locked: false,
      baseUrl: 'http://127.0.0.1:5000',
      errorMsg: null
    };
  },
  async mounted() {
    try {
      const connectionStatusResponse = await axios.get(`${this.baseUrl}/getConnectionStatus`);
      if (connectionStatusResponse.data.connected === 'true') {
        this.connected = true;
        const lockStatusResponse = await axios.get(`${this.baseUrl}/getLockStatus`);
        this.locked = lockStatusResponse.data.locked === 'true';
      }
    } catch (error) {
      this.errorMsg = 'Whoops, something went wrong';
    }
  },
  methods: {
    async lockDevice() {
      try {
        const response = await axios.post(`${this.baseUrl}/lock`);
        if (response.status === 201) {
          this.locked = true;
        }
      } catch (_) {
        this.errorMsg = 'Whoops, something went wrong when locking device';
      }
    },
    async unlockDevice() {
      try {
        const response = await axios.post(`${this.baseUrl}/unlock`);
        if (response.status === 201) {
          this.locked = false;
        }
      } catch (_) {
        this.errorMsg = 'Whoops, something went wrong when unlocking device';
      }
    }
  }
};
</script>
