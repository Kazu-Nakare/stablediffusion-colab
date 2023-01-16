<template>
  <v-container fluid class="fill-height align-stretch">
    <v-row>
      <v-col cols="4" class="d-flex flex-column">
        <v-card>
          <v-textarea outlined hide-details disabled :value="total_prompt">
          </v-textarea>
        </v-card>
        <v-card>
          <v-text-field
            v-model="prompt"
            outlined
            hide-details
            label="Prompt"
            placeholder="A photo of an astronaut riding a horse"
            clearable
            clear-icon="mdi-close-circle"
            prepend-inner-icon="mdi-comment-text"
            :disabled="loading">
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
        </v-card>
        <v-card class="pa-2 flex-grow-1 overflow-auto">
          <v-container>
            <draggable animation="300" v-model="tags">
              <div v-for="(tag, i) in tags" :key="tag" class="d-inline-flex">
                <v-menu offset-y transition="scale-transition" origin="top left">
                  <template v-slot:activator="{ on }">
                    <v-chip v-on="on" close @click:close="tags.splice(i, 1)">
                      <v-avatar left color="primary" class="mr-1">
                        <span class="white--text font-weight-black">+1</span>
                      </v-avatar>
                      {{ tag }}
                    </v-chip>
                  </template>
                  <v-card>
                    {{ tag }}
                  </v-card>
                </v-menu>
              </div>
            </draggable>
            <v-menu offset-y top left :close-on-content-click="false" transition="scale-transition" origin="bottom right">
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" fab color="blue" absolute right dark :ripple="false" style="bottom:20px">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <v-card class="pa-2">
                <v-text-field
                  v-model="prompt"
                  outlined
                  hide-details
                  label="New Tag"
                  placeholder="A photo of an astronaut riding a horse"
                  clearable
                  clear-icon="mdi-close-circle"
                  prepend-inner-icon="mdi-comment-text">
                  <template v-slot:append-outer>
                    <v-icon @click="log($parent)">
                      mdi-send
                    </v-icon>
                  </template>
                </v-text-field>
              </v-card>
            </v-menu>
          </v-container>
        </v-card>
      </v-col>
      <v-col class="info">
        <div v-for="image in images" :key="image">
          <a :href="image.url" :download="image.prompt">
            <img :src="image.url" :title="image.prompt" />
          </a>
        </div>
      </v-col>
      <v-col cols="2" class="white">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import draggable from 'vuedraggable'

  export default {
    name: 'HelloWorld',
    components: {
    'draggable': draggable,
    },
    data () {
      return {
        prompt: "",
        images: [],
        loading: false,
        tags: ["aaaa", "bbbbb", "ccca", "dddddddd", "jgosjgoahoih"],
      }
    },
    methods: {
      log(parent) {
        console.log(parent.target.value)
      },
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
      end(e) {
        console.log(e.oldIndex)
        console.log(e.newIndex)
        console.log(e.to.textContent)
        this.tags = e.to
        console.log(this.tags)
      }
    },
    computed: {
      total_prompt() {
        return this.tags.join(', ')
      }
    }
  }

</script>

