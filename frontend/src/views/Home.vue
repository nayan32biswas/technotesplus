<template>
  <div v-if="note" class="container mt-3">
    <note-list :notes="note.results" />
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

import { FETCH_NOTES } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import NoteList from "../components/NoteList.vue";
import { totalPages } from "../utils/utils";
import { ObjectType } from "@/type/additionalApi.types";

export const DEFAULT_PARAMS: any = {
  limit: 10,
  offset: 0,
  search: "",
};

@Component({
  components: {
    NoteList,
  },
})
export default class Home extends Vue {
  @CommonModule.Action [FETCH_NOTES]: any;

  note: any = null;
  filter = JSON.parse(JSON.stringify(DEFAULT_PARAMS));

  get page(): number {
    return this.$route.query.page
      ? parseInt(this.$route.query.page as string)
      : 1;
  }
  get pages(): number {
    return totalPages(this.note.count, this.filter.limit);
  }
  @Watch("filter", { deep: true, immediate: true })
  handleFilterChange(val: ObjectType, oldVal: ObjectType): void {
    this.getNotes();
  }
  handlePageChange(pgNum: number): void {
    if (pgNum > 1) {
      this.filter.offset = pgNum - 1;
      const query = { page: pgNum.toString() };
      this.$router.replace({ path: this.$route.path, query });
    } else {
      this.filter.offset = 0;
      this.$router.replace({ path: this.$route.path });
    }
  }

  getNotes(): void {
    this[FETCH_NOTES]({ filter: this.filter }).then((data: any) => {
      this.note = data;
    });
  }

  mounted(): void {
    if (this.page) {
      this.filter.offset = this.page - 1;
    }
    this.getNotes();
  }
}
</script>

<style scoped lang="scss"></style>
