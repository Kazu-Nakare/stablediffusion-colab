<template>
  <div id="app">
    <h1>Hello World</h1>
    <img alt="Vue logo" src="./assets/logo.png" />
    <textarea v-model="prompt"></textarea>
    <button type="button" @click="test">送信</button>
    <div v-for="image in images" :key="image">
      <a :href="image.url" :download="image.prompt">
        <img :src="image.url" :title="image.prompt" />
      </a>
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
        images: []
      };
    },
    methods: {
      test() {
        axios
          .post("/generate", {
              prompt: this.prompt,
            },
            {
              responseType: 'blob',
            })
          .then((response) => {
            console.log(response)

            let src = URL.createObjectURL(response.data)
            console.log(src)

            this.images.push({url: src, prompt: this.prompt})
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
