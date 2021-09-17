<template>
  <div v-if="note">
    <div>{{ note.name }}</div>
    <div v-html="note.content"></div>
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
