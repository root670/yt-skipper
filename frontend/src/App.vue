<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-toolbar-title>yt-skipper</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-app-bar>

    <v-content>
      <CaptionTagger />
    </v-content>
  </v-app>
</template>

<script>
import CaptionTagger from './components/CaptionTagger/CaptionTagger';

export default {
  name: 'App',

  components: {
    CaptionTagger
  },

  data: () => ({
    //
  }),
};
</script>
