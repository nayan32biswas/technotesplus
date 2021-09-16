<template>
  <div v-if="note">
    <b-card
      :title="note.name"
      img-alt="Image"
      img-top
      tag="article"
      style="max-width: 20rem"
      class="mb-2"
    >
      <b-card-text>{{ note.short_content }} </b-card-text>
      <router-link
        :to="{ name: 'NoteDetails', params: { slug: note.slug } }"
        class="details-btn"
        ><b-button class="primary">Details</b-button></router-link
      >
    </b-card>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class NoteCard extends Vue {
  @Prop() note!: any;
}
</script>

<style scoped lang="scss">
.details-btn {
  color: black !important;
}
</style>
