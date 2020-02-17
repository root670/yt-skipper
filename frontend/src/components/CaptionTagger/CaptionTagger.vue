<template>
<v-container>
  <v-row>

  <v-col cols="12" sm="6">
    <v-text-field
      v-model="videoUrl"
      label="Video URL"
      single-line
      @keydown.enter="fetchCaption"
    ></v-text-field>
    <v-btn
      color="primary"
      :loading="loading"
      :disabled="loading"
      @click="fetchCaption"
    >
      Fetch
    </v-btn>
  </v-col>

  </v-row>
  <v-row>
    <Captions
      :data="captions"
      ></Captions>
  </v-row>
</v-container>
</template>

<script>

import axios from 'axios';
import { API_URL } from '@/constants.js';
import Captions from './Captions';

const VIDEO_ID_REGEX = "^.*(?:youtu.be/|v/|e/|u/w+/|embed/|v=)([^#&?]*).*";

export default {
    name: 'CaptionTagger',
    components: {
      Captions
    },
    data: function() {
      return {
        videoUrl: '',
        captions: [],
        loading: false,
      }
    },
    computed: {
      videoId() {
        let match = this.videoUrl.match(VIDEO_ID_REGEX);
        return (match == null) ? '' : match[1];
      }
    },
    methods: {
      fetchCaption() {
        if (this.videoId == '')
          return;

        this.loading = true;
        this.captions = [];

        axios.get(API_URL + '/' + this.videoId)
          .then((response) => {
            this.captions = response.data;
          })
          .catch((error) => {
            console.log(error)
          })
          .finally(() => {
            this.loading = false;
          });
      }
    }
}
</script>

<style scoped>

</style>