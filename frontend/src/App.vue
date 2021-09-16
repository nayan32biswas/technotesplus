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

// a {
//   color: rgb(64 53 121) !important;
// }
.router-link-exact-active {
  color: rgb(64 53 121) !important;
}
</style>
