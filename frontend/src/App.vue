<template>
  <div id="app">
    <h1>Hello World</h1>
    <img alt="Vue logo" src="./assets/logo.png" />
    <textarea v-model="prompt"></textarea>
    <button type="button" @click="test">送信</button>
    <div v-for="image in images" :key="image">
      <a :href="image.url" :download="prompt">
        <img :src="image.url" :title="prompt" />
      </a>
    <a :href="url">go</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "App",
  data() {
      return {
        prompt: "",
        url: "",
        images: []
      };
    },
    methods: {
      test() {
        axios
          .post("/generate", {
            prompt: this.prompt,
          })
          .then((response) => {
            console.log(response)
            let blob = new Blob([response.data], { type: 'image/png' })
            console.log(blob)
            // let reader = new FileReader();
            // reader.readAsDataURL(blob);
            // let src = ""
            // reader.onload = function() {
            //   src = reader.result
            // }
            let src = URL.createObjectURL(blob)
            console.log(src)

            this.url = src
            // this.images.push({url: src})
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
