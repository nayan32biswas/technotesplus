<template>
  <div>
    <b-row>
      <b-col
        lg="4"
        xl="4"
        md="6"
        sm="6"
        cols="12"
        v-for="note in notes"
        :key="'note-' + note.slug"
      >
        <NoteCard :note="note" />
      </b-col>
    </b-row>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import NoteCard from "./NoteCard.vue";

@Component({
  components: {
    NoteCard,
  },
})
export default class NoteList extends Vue {
  @Prop() notes!: any[];
}
</script>

<style scoped lang="scss"></style>
