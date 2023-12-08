<template>
  <p>{{ msg }}</p>
</template>

<script>
import mqtt from 'mqtt';

export default {
  data() {
    return {
      msg: ''
    };
  },
  mounted() {
    const client = mqtt.connect('mqtt://test.mosquitto.org');

    client.on('connect', () => {
      client.subscribe('presence', (err) => {
        if (!err) {
          client.publish('presence', 'Hello mqtt');
        }
      });
    });

    client.on('message', (topic, message) => {
      // message is Buffer
      console.log(message.toString());
      client.end();
    });
  }
};
</script>
