<template>
  <div v-if="note" class="container mt-3">
    <b-form-input
      v-model="filter.search"
      debounce="300"
      placeholder="Enter query"
    ></b-form-input>
    <note-list :notes="note.results" details-page="ShareWithMeNoteDetails" />
    <b-pagination
      first-number
      last-number
      pills
      :value="page"
      :per-page="filter.limit"
      :total-rows="note.count"
      align="center"
      :hide-ellipsis="true"
      prev-text="<"
      next-text=">"
      :number-of-pages="pages"
      @change="handlePageChange"
    ></b-pagination>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from "vue-property-decorator";

import { FETCH_SHARE_NOTES } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import NoteList from "../components/NoteList.vue";
import { totalPages } from "../utils/utils";
import { ObjectType } from "@/type/additionalApi.types";

export const DEFAULT_PARAMS: any = {
  limit: 2,
  offset: 0,
  search: "",
};

@Component({
  components: {
    NoteList,
  },
})
export default class ShareWithMeNote extends Vue {
  @CommonModule.Action [FETCH_SHARE_NOTES]: any;

  filter = JSON.parse(JSON.stringify(DEFAULT_PARAMS));
  filterParams: any | null = JSON.parse(JSON.stringify(DEFAULT_PARAMS));

  search = "";
  note: any = null;

  get page(): number {
    return this.$route.query.page
      ? parseInt(this.$route.query.page as string)
      : 1;
  }
  offset(page: number): number {
    return page * this.filter.limit;
  }
  get pages(): number {
    return totalPages(this.note.count, this.filter.limit);
  }
  @Watch("filter", { deep: true, immediate: true })
  handleFilterChange(val: ObjectType, oldVal: ObjectType): void {
    const data = JSON.parse(JSON.stringify(val));
    if (val.search.trim().length == 0) {
      delete data.search;
    } else {
      data.offset = 0;
      // this.filter.offset = 0;
      this.$router.replace({ path: this.$route.path });
    }
    this.filterParams = {
      ...data,
    };
  }
  @Watch("filterParams", { deep: true })
  handleFilterParamsChange(): void {
    this.getNotes();
  }
  handlePageChange(pgNum: number): void {
    if (pgNum > 1) {
      this.filter.offset = this.offset(pgNum - 1);
      const query = { page: pgNum.toString() };
      this.$router.replace({ path: this.$route.path, query });
    } else {
      this.filter.offset = 0;
      this.$router.replace({ path: this.$route.path });
    }
  }

  getNotes(): void {
    this[FETCH_SHARE_NOTES]({ filter: this.filterParams }).then((data: any) => {
      this.note = data;
    });
  }

  mounted(): void {
    if (this.page) {
      this.filter.offset = this.offset(this.page - 1);
    }
    this.getNotes();
  }
}
</script>

<style scoped lang="scss"></style>
