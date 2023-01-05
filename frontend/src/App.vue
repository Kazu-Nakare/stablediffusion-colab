<template>
  <div id="app">
    <h1>Hello World</h1>
    <img alt="Vue logo" src="./assets/logo.png" />
    <input v-model="title" />
    <textarea v-model="content"></textarea>
    <button type="button" @click="test">送信</button>
    <p>あいうえお ＆ {{ posts }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "App",
  data() {
      return {
        title: "",
        content: "",
        posts: ""
      };
    },
    methods: {
      test() {
        axios
          .post("/test", {
            title: this.title,
            content: this.content,
          })
          .then((res) => {
            this.posts = res.data.data;
            console.log(this.posts);
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
