<template>
  <div>
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-form @submit.prevent="handleSubmit(noteSubmit)">
        <ValidationProvider v-slot="{ errors, touched }" rules="required">
          <div>
            <label>Name</label>
            <div>
              <input
                type="text"
                placeholder="Enter Name"
                name="Name"
                v-model="noteForm.name"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider v-slot="{ errors, touched }" rules="required">
          <div class="mt-3">
            <label>Content</label>
            <vue-editor v-model="noteForm.content" name="Content"></vue-editor>
          </div>
          <span v-if="touched && errors.length > 0" class="text-danger">{{
            errors[0]
          }}</span>
        </ValidationProvider>

        <ValidationProvider v-slot="{ errors, touched }" rules="required">
          <div class="mt-2">
            <label>Tags(Use "," Comma after one tag)</label>
            <b-form-tags v-model="noteForm.tags" separator=","></b-form-tags>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <div class="mt-2">
          <b-button @click.prevent="$emit('cancel')" class="mr-1"
            >Cancel</b-button
          >
          <b-button type="submit">Save</b-button>
        </div>
      </b-form>
    </ValidationObserver>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import { VueEditor } from "vue2-editor";
import { CREATE_OR_UPDATE_NOTE } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import { AxiosError } from "axios";

const DEFAULT_LOGIN_FORM = {
  name: "",
  content: "",
  tags: [],
};
@Component({ components: { VueEditor } })
export default class NoteForm extends Vue {
  @Prop() note!: any;
  @CommonModule.Action [CREATE_OR_UPDATE_NOTE]: any;

  noteForm = JSON.parse(JSON.stringify(DEFAULT_LOGIN_FORM));

  noteSubmit(): void {
    console.log("note submit");
    if (this.noteForm.tags.length == 0) {
      alert("Please provide tags");
    } else {
      this[CREATE_OR_UPDATE_NOTE]({
        payload: this.noteForm,
        slug: this.note?.slug,
      })
        .then((data: any) => {
          this.$emit("saved", data);
        })
        .catch((e: AxiosError) => {
          console.log(e);
        });
    }
  }

  mounted(): void {
    if (this.note?.slug) {
      this.noteForm = { ...this.note };
    }
  }
}
</script>

<style scoped lang="scss"></style>
