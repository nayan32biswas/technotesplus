<template>
  <div class="container mt-3">
    <NoteForm @cancel="cancel" @saved="saved" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NoteForm from "../components/NoteForm.vue";

@Component({ components: { NoteForm } })
export default class NoteCreate extends Vue {
  cancel(): void {
    alert("Something wrong");
  }
  saved(note: any): void {
    this.$router.push({ name: "NoteDetails", params: { slug: note.slug } });
  }
}
</script>

<style scoped lang="scss"></style>
