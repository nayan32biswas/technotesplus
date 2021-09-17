<template>
  <div v-if="note">
    <div v-if="!editNote">
      <div>
        <b-button @click.prevent="editNote = true">Edit</b-button>
        <b-button @click.prevent="deleteNoteSubmit">Delete</b-button>
        <b-button @click.prevent="showShareModal = true">Share</b-button>
      </div>
      <div>{{ note.name }}</div>
      <div v-html="note.content"></div>
    </div>
    <div v-else>
      <NoteForm :note="note" @cancel="cancel" @saved="saved" />
    </div>
    <b-modal centered hide-footer hide-header v-model="showShareModal">
      <div>
        <h4>Share Note With Other user</h4>
        <v-select
          @search="handleUserSearch"
          :options="userSearch"
          v-model="selectedUsers"
          :taggable="false"
          multiple
          label="full_name"
          placeholder="Add Users"
          class="inputBorder hide-user mt-2"
        >
        </v-select>
        <div>
          <b-button type="submit" @click.prevent="shareNoteSubmit"
            >Share</b-button
          >
        </div>

        <div>
          <b-table
            v-if="note.viewers.length"
            striped
            hover
            :responsive="true"
            :items="note.viewers"
            :fields="viewerFields"
            class="justify-content-center mb-1"
          >
            <template #cell(Remove)="data">
              <b-button
                size="sm"
                class="CustomBtn edit-btn"
                @click.prevent="removeUserSubmit(data.item.username)"
              >
                <b-button>Remove</b-button>
              </b-button>
            </template>
          </b-table>
        </div>
      </div>
    </b-modal>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import vSelect from "vue-select";
import {
  DELETE_NOTE,
  FETCH_NOTE_DETAILS,
  FETCH_PUBLIC_USER,
  REMOVE_NOTE_USER,
  SHARE_NOTE,
} from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import NoteForm from "../components/NoteForm.vue";

@Component({ components: { NoteForm, vSelect } })
export default class NoteDetails extends Vue {
  @CommonModule.Action [FETCH_NOTE_DETAILS]: any;
  @CommonModule.Action [FETCH_PUBLIC_USER]: any;
  @CommonModule.Action [DELETE_NOTE]: any;
  @CommonModule.Action [SHARE_NOTE]: any;
  @CommonModule.Action [REMOVE_NOTE_USER]: any;

  note: any = null;
  editNote = false;
  showShareModal = false;

  selectedUsers = [];
  userSearch: any[] = [];

  viewerFields = [
    { key: "full_name", label: "Full Name" },
    { key: "username", label: "Usrename" },
    "Remove",
  ];

  handleUserSearch(e: any): void {
    this[FETCH_PUBLIC_USER]({ search: e }).then((data: any) => {
      this.userSearch = data.results;
    });
  }

  shareNoteSubmit(): void {
    const payload = {
      users: this.selectedUsers.map((user: any) => user.username),
    };
    if (payload.users.length) {
      this[SHARE_NOTE]({ slug: this.slug, payload }).then((data: any) => {
        alert("Note Shared with users.");
        this.showShareModal = false;
      });
    }
  }
  removeUserSubmit(username: string): void {
    if (username) {
      this[REMOVE_NOTE_USER]({
        slug: this.slug,
        payload: { user: username },
      }).then((data: any) => {
        alert("User removed from list.");
        this.showShareModal = false;
      });
    }
  }

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

  deleteNoteSubmit(): void {
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
