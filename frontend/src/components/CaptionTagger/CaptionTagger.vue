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
  <v-container fluid>
    <v-row dense ref="selectable">
      <span
        v-for="(caption, idx) in captions"
        :key="idx"
        :id="idx"
        class="word lighten-4"
        :class="{
          purple: caption.tag == DEFAULT_TEXT_LABEL,
          green: caption.tag == TEXT_LABELS.SPONSOR_MENTION
        }"
      >{{ caption.word }}</span>
    </v-row>
  </v-container>
</v-container>
</template>

<script>

import axios from 'axios';
import { API_URL, DEFAULT_TEXT_LABEL, TEXT_LABELS } from '@/constants.js';

const VIDEO_ID_REGEX = "^.*(?:youtu.be/|v/|e/|u/w+/|embed/|v=)([^#&?]*).*";

export default {
    name: 'CaptionTagger',
    data: function() {
      return {
        videoUrl: '',
        captions: [],
        loading: false,
        DEFAULT_TEXT_LABEL: DEFAULT_TEXT_LABEL,
        TEXT_LABELS: TEXT_LABELS
      }
    },
    computed: {
      videoId() {
        let match = this.videoUrl.match(VIDEO_ID_REGEX);
        return (match == null) ? '' : match[1];
      }
    },
    mounted () {
    window.addEventListener('mouseup', this.onMouseup)
    },

    beforeDestroy () {
      window.removeEventListener('mouseup', this.onMouseup)
    },
    methods: {
      onMouseup() {
        console.log('Mouse up');
        const selection = window.getSelection();
        const startNode = selection.getRangeAt(0).startContainer.parentNode;
        const endNode = selection.getRangeAt(0).endContainer.parentNode;
        if(startNode.parentNode == this.$refs["selectable"])
        {
          console.log('start:' + startNode.id);
          console.log('end:' + endNode.id);
          selection.removeAllRanges();
        }
      },
      fetchCaption() {
        if (this.videoId == '')
          return;

        this.loading = true;
        this.captions = [];

        axios.get(API_URL + '/' + this.videoId)
          .then((response) => {
            this.captions = response.data.map(obj => ({
              ...obj, tag: DEFAULT_TEXT_LABEL
            }));
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
.word {
  margin-right: 1em;
}
</style>