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
        :disabled="loading || videoUrl.length == 0"
        @click="fetchCaption"
      >Fetch</v-btn>
    </v-col>
  </v-row>
    <v-alert v-if="errorText.length > 0" type="error">{{ errorText }}</v-alert>
  <v-row dense ref="selectable">
    <div
      v-show="showTools"
      class="tools"
      :style="{
        left: `${toolsX}px`,
        top: `${toolsY}px`,
      }"
      ></div>
    <span
      v-for="(caption, idx) in captions"
      :key="idx"
      :id="idx"
      class="word lighten-4"
      :class="{
        /*purple: caption.tag == DEFAULT_TEXT_LABEL,*/
        green: caption.tag == TEXT_LABELS.SPONSOR_MENTION
      }"
    >{{ caption.word }}</span>
  </v-row>
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
        TEXT_LABELS: TEXT_LABELS,
        errorText: '',
        showTools: false,
        toolsX: 0,
        toolsY: 0
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
        const selection = window.getSelection();
        const startContainer = selection.getRangeAt(0).startContainer;
        const endContainer = selection.getRangeAt(0).endContainer;
        let startNode = (startContainer.nodeType == Node.TEXT_NODE) ? startContainer.parentNode : startContainer;
        let endNode = (endContainer.nodeType == Node.TEXT_NODE) ? endContainer.parentNode : endContainer;
        if(startNode.parentNode == this.$refs["selectable"] && endNode.parentNode == this.$refs["selectable"]) {
          console.log('start:' + startNode.id);
          console.log('end:' + endNode.id);

          const { x, y, width } = selection.getRangeAt(0).getBoundingClientRect();
          if(!width) {
            this.showTools = false;
            return
          }
          this.toolsX = x + (width / 2);
          this.toolsY = y + window.scrollY - 75;
          this.showTools = true;
          // selection.removeAllRanges();
        }
      },
      fetchCaption() {
        if (this.videoId == '')
        {
          this.errorText = "Couldn't get video ID from URL.";
          return;
        }

        this.loading = true;
        this.captions = [];
        this.errorText = '';

        axios.get(API_URL + '/' + this.videoId)
          .then((response) => {
            this.captions = response.data.map(obj => ({
              ...obj, tag: DEFAULT_TEXT_LABEL
            }));
          })
          .catch((error) => {
            console.log(error);
            this.errorText = error.response.data.error;
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
  padding-left: .5em;
  padding-right: .5em;
}
.tools {
  position: absolute;
  background: red;
  width: 50px;
  height: 20px;
}
</style>