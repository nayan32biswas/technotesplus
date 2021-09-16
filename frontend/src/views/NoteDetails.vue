<template>
  <div v-if="note">
    <div v-if="!editNote">
      <div>
        <b-button @click.prevent="editNote = true">Edit</b-button>
        <b-button @click.prevent="deleteNoteSubmit">Delete</b-button>
      </div>
      <div>{{ note.name }}</div>
      <div v-html="note.content"></div>
    </div>
    <div v-else>
      <NoteForm :note="note" @cancel="cancel" @saved="saved" />
    </div>
  </div>
</template>

<script lang="ts">
import { DELETE_NOTE, FETCH_NOTE_DETAILS } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import { Component, Vue } from "vue-property-decorator";
import NoteForm from "../components/NoteForm.vue";

@Component({ components: { NoteForm } })
export default class NoteDetails extends Vue {
  @CommonModule.Action [FETCH_NOTE_DETAILS]: any;
  @CommonModule.Action [DELETE_NOTE]: any;

  note: any = null;
  editNote = false;

  get slug(): string {
    return this.$route.params.slug;
  }

  cancel(): void {
    this.editNote = false;
  }
  saved(note: any): void {
    this.editNote = false;
    this.note = note;
  }

  deleteNoteSubmit() {
    alert("Do you want to delete the note?");
    this[DELETE_NOTE]({ slug: this.slug }).then((data: any) => {
      this.$router.push({ name: "Home" });
    });
  }

  mounted(): void {
    this[FETCH_NOTE_DETAILS]({ slug: this.slug }).then((data: any) => {
      this.note = data;
    });
  }
}
</script>

<style scoped lang="scss"></style>
