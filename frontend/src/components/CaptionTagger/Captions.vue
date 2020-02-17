<template>
    <v-content>
        <v-row>
            {{ captionText }}
        </v-row>
    </v-content>
</template>

<script>
export default {
    name: 'Captions',
    props: {
        data: Array
    },
    computed: {
        captionText() {
            return this.data.map(e => e.text).join(' ');
        }
    }
}
</script>

<style scoped>

</style>