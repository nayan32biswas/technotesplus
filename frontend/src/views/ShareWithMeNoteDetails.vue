<template>
  <div v-if="note" class="container mt-3">
    <div>
      <h4>Name: {{ note.name }}</h4>
    </div>
    <div class="content">
      <div v-html="note.content"></div>
    </div>
    <div>
      <span>Tags: </span>
      <span
        v-for="tag in note.tags"
        class="tags"
        :key="note.slug + '-tag-' + tag"
        >{{ tag }}</span
      >
    </div>
  </div>
</template>

<script lang="ts">
import { FETCH_SHARE_NOTE_DETAILS } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import { Component, Vue } from "vue-property-decorator";
import NoteForm from "../components/NoteForm.vue";

@Component({ components: { NoteForm } })
export default class ShareWithMeNoteDetails extends Vue {
  @CommonModule.Action [FETCH_SHARE_NOTE_DETAILS]: any;

  note: any = null;
  editNote = false;

  get slug(): string {
    return this.$route.params.slug;
  }

  mounted(): void {
    this[FETCH_SHARE_NOTE_DETAILS]({ slug: this.slug }).then((data: any) => {
      this.note = data;
    });
  }
}
</script>

<style scoped lang="scss"></style>
