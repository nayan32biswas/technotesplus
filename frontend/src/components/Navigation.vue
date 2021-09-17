<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand
        ><router-link :to="{ name: 'Home' }">Home</router-link></b-navbar-brand
      >

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto ml-2">
          <b-nav-item v-if="authenticated">
            <router-link :to="{ name: 'ShareWithMeNote' }"
              >Share With Me</router-link
            >
          </b-nav-item>
          <b-nav-item v-if="authenticated">
            <router-link :to="{ name: 'NoteCreate' }">Create Note</router-link>
          </b-nav-item>
          <b-nav-item v-if="authenticated">
            <router-link :to="{ name: 'Profile' }">Profile</router-link>
          </b-nav-item>
          <b-nav-item v-if="authenticated">
            <a @click.prevent="logoutUser">Logout</a>
          </b-nav-item>

          <b-nav-item v-if="!authenticated">
            <router-link :to="{ name: 'Login' }">Login</router-link>
          </b-nav-item>
          <b-nav-item v-if="!authenticated">
            <router-link :to="{ name: 'Signup' }">Signup</router-link>
          </b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { AUTHENTICATED } from "@/store/getter.names";
import { CommonModule } from "@/store/namespace.names";
import { LOGOUT } from "@/store/action.names";

@Component
export default class Navigation extends Vue {
  @CommonModule.Getter(AUTHENTICATED) authenticated: any;
  @CommonModule.Action [LOGOUT]: any;

  logoutUser(): void {
    this[LOGOUT]().then(() => {
      this.$router.push({ name: "Login" });
    });
  }
}
</script>

<style scoped lang="scss"></style>
