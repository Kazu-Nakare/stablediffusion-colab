<template>
  <v-container fluid class="fill-height align-stretch">
    <v-row>
      <v-col cols="4" class="d-flex flex-column">
        <v-card class="mb-1">
          <v-textarea outlined hide-details readonly :value="total_prompt">
          </v-textarea>
          <v-btn icon v-clipboard:copy="total_prompt" v-clipboard:success="() => snackbar=true">
            <v-icon>
              mdi-clipboard-text-multiple-outline
            </v-icon>
          </v-btn>
          <v-snackbar top color="green" v-model="snackbar" timeout="3000" transition="slide-y-transition">
            Copyed!
            <template v-slot:action="{ attrs }">
              <v-btn icon v-bind="attrs" @click="snackbar = false">
                <v-icon>
                  mdi-close
                </v-icon>
              </v-btn>
            </template>
          </v-snackbar>
          <v-progress-circular
            v-if="loading"
            size="24"
            color="info"
            indeterminate
          ></v-progress-circular>
          <v-btn v-else @click="generate">
            Generate
          </v-btn>
        </v-card>
        <v-card class="mb-1 flex-grow-1 overflow-auto">
          <v-container>
            <draggable animation="300" v-model="tags">
              <div v-for="(tag, i) in tags" :key="tag.context" class="d-inline-flex ma-1">
                <v-menu
                  offset-y
                  :close-on-content-click="false"
                  transition="scale-transition"
                  origin="top left">
                  <template v-slot:activator="{ on }">
                    <v-chip v-on="on" close @click:close="tags.splice(i, 1)">
                      <v-avatar v-if="tag.bracket" left :color="(tag.bracket > 0) ? 'primary' : 'red'" class="mr-1">
                        <span class="white--text font-weight-black">
                          {{ (tag.bracket > 0) ? "+" + tag.bracket : tag.bracket }}
                        </span>
                      </v-avatar>
                      {{ tag.context }}
                    </v-chip>
                  </template>
                  <v-card class="d-flex flex-row pa-2">
                    <v-text-field
                      v-model.number="tags[i].bracket"
                      type="number"
                      style="width: 60px"
                      outlined
                      hide-details>
                    </v-text-field>
                    <v-text-field
                      :value="tags[i].context"
                      outlined
                      hide-details
                      label="Tag"
                      placeholder="house"
                      prepend-inner-icon="mdi-comment-text">
                      <template v-slot:append-outer>
                        <v-icon @click="log(tag)">
                          mdi-send
                        </v-icon>
                      </template>
                    </v-text-field>
                  </v-card>
                </v-menu>
              </div>
            </draggable>
            <v-menu
              offset-y
              top left
              :close-on-content-click="false"
              transition="scale-transition"
              origin="bottom right">
              <template v-slot:activator="{ on }">
                <v-btn v-on="on" fab color="blue" absolute right dark :ripple="false" style="bottom:20px">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </template>
              <v-card class="pa-2">
                <v-text-field
                  v-model="newtag"
                  outlined
                  hide-details
                  label="New Tag"
                  placeholder="A photo of an astronaut riding a horse"
                  clearable
                  clear-icon="mdi-close-circle"
                  prepend-inner-icon="mdi-comment-text">
                  <template v-slot:append-outer>
                    <v-icon @click="log(newtag)">
                      mdi-send
                    </v-icon>
                  </template>
                </v-text-field>
              </v-card>
            </v-menu>
          </v-container>
        </v-card>
        <v-card>
          <v-text-field
            v-model="newprompt"
            outlined
            hide-details
            label="Prompt"
            placeholder="A photo of an astronaut riding a horse"
            clearable
            clear-icon="mdi-close-circle"
            prepend-inner-icon="mdi-comment-text"
            :disabled="loading">
            <template v-slot:append-outer>
              <v-btn @click="insert">
                Insert
              </v-btn>
            </template>
          </v-text-field>
        </v-card>
      </v-col>
      <v-col class="info">
        <div v-for="image in images" :key="image">
          <a :href="image.url" :download="image.total_prompt">
            <v-img contain :src="image.url" :title="image.total_prompt"></v-img>
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
        newprompt: "",
        newtag: "",
        images: [],
        loading: false,
        snackbar: false,
        tags: [{bracket: -3, context: "aaaa"}]
      }
    },
    methods: {
      log(tag) {
        if (this.newtag) {
          this.tags.push({bracket: 0, context: tag})
          this.newtag = ""
        }
      },
      insert() {
        if (this.newprompt) {
          let prompt = this.newprompt.split(',').map((e)=>e.trim())
          let newtags = []

          prompt.forEach((pmt)=>{
            const re_p = /\{(.+)\}/
            const re_m = /\[(.+)\]/
            let cnt = 0
            while (pmt.match(re_p) || pmt.match(re_m)) {
              if (pmt.match(re_p)) {
                cnt++
                pmt = pmt.match(re_p)[1]
              } else {
                cnt--
                pmt = pmt.match(re_m)[1]
              }
            }
            newtags.push({bracket: cnt, context: pmt})
          })

          this.tags = this.tags.concat(newtags)
          this.newprompt = ""
        }
      },
      prom_gen(tag) {
        let result = tag.context
        if (tag.bracket > 0) {
          result = "{".repeat(tag.bracket) + result + "}".repeat(tag.bracket)
        } else if (tag.bracket < 0) {
          result = "[".repeat(-tag.bracket) + result + "]".repeat(-tag.bracket)
        }
        return result
      },
      generate() {
        this.loading = true
        axios
          .post("/generate",
            { prompt: this.total_prompt },
            { responseType: 'blob', })
          .then((response) => {
            this.loading = false

            let src = URL.createObjectURL(response.data)

            this.images.push({url: src, prompt: this.prompt})
          })
          .catch((err) => {
            console.log(err);
          });
      },
    },
    computed: {
      total_prompt() {
        return this.tags.map((e)=>this.prom_gen(e)).join(', ')
      }
    }
  }

</script>

