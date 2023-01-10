<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-icon x-large class="mr-2">mdi-palette-advanced</v-icon>

        <h2>Stable Diffusion Colab</h2>
      </div>

      <v-spacer></v-spacer>

        <div class="font-weight-medium align-self-center">V0.1.4</div>
    </v-app-bar>

    <v-main>
      <Generator/>
    </v-main>
  </v-app>
</template>

<script>
import Generator from './components/Generator';

export default {
  name: 'App',

  components: {
    Generator,
  },

  data: () => ({
    //
  }),
};
</script>
