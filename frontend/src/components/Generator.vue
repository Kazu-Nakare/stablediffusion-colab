<template>
  <div class="mx-auto mt-3 mb-6 text-center" style="width:600px;">
    <v-text-field
      v-model="prompt"
      outlined
      label="Prompt"
      placeholder="A photo of an astronaut riding a horse"
      clearable
      clear-icon="mdi-close-circle"
      prepend-inner-icon="mdi-comment-text"
      :disabled="loading"
    >
      <template v-slot:append-outer>
        <v-progress-circular
          v-if="loading"
          size="24"
          color="info"
          indeterminate
        ></v-progress-circular>
        <v-icon v-else @click="generate">
          mdi-send
        </v-icon>
      </template>
    </v-text-field>
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
    name: 'HelloWorld',
    data () {
      return {
        prompt: "",
        images: [],
        loading: false,
      }
    },
    methods: {
      generate() {
        this.loading = true
        axios
          .post("/generate", {
              prompt: this.prompt,
            },
            {
              responseType: 'blob',
            })
          .then((response) => {
            this.loading = false
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
  }

</script>

