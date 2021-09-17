<template>
  <div id="app">
    <Navigation />
    <router-view />
  </div>
</template>
<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import Navigation from "./components/Navigation.vue";

@Component({
  components: {
    Navigation,
  },
})
export default class App extends Vue {}
</script>

<style lang="scss">
@import "@/assets/style/main.scss";
@import "../node_modules/bootstrap/scss/bootstrap.scss";
@import "../node_modules/bootstrap-vue/dist/bootstrap-vue.css";

input {
  padding: 10px !important;
}

.router-link-exact-active {
  color: rgb(64 53 121) !important;
}

.custom-search-box {
  max-width: 350px;
  display: flex;
  justify-content: center;
}
.content {
  margin: 0;
  background-color: #f6f6f6;
  font-weight: 400;
  padding: 10px 20px;
  margin-bottom: 15px;
  border-radius: 5px;
}
.tags {
  background-color: #abafb1;
  padding: 4px 10px;
  border-radius: 5px;
  margin-right: 3px;
}
</style>
