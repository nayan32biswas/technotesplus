<template>
  <div
    class="d-flex align-items-center justify-content-center signup-container"
  >
    <ValidationObserver v-slot="{ handleSubmit }">
      <b-form @submit.prevent="handleSubmit(userSubmit)">
        <ValidationProvider v-slot="{ errors, touched }" rules="required|email">
          <div>
            <label>Email</label>
            <div>
              <input
                type="email"
                placeholder="Enter Email"
                name="Email"
                v-model="signupForm.email"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider v-slot="{ errors, touched }" rules="required">
          <div class="mt-2">
            <label>Username</label>
            <div>
              <input
                type="text"
                placeholder="Enter Username"
                name="Username"
                v-model="signupForm.username"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider
          v-slot="{ errors, touched }"
          rules="required|min:8"
          vid="confirm_password"
        >
          <div class="mt-2">
            <label>Password</label>
            <div>
              <input
                type="password"
                placeholder="Enter Password"
                name="Password"
                v-model="signupForm.password"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <ValidationProvider
          v-slot="{ errors, touched }"
          rules="required|confirmed:confirm_password"
          vid="password2"
        >
          <div class="mt-2">
            <label>Confirm Password</label>
            <div>
              <input
                type="password"
                placeholder="Enter Confirm Password"
                name="Confirm Password"
                v-model="signupForm.confirm_password"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </div>
        </ValidationProvider>

        <div class="mt-3">
          <b-button type="submit">Create Account</b-button>
        </div>
      </b-form>
    </ValidationObserver>
    <router-link :to="{ name: 'Login' }">Login</router-link>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { SIGNUP } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";

const DEFAULT_SIGNUP_FORM = {
  username: "",
  email: "",
  password: "",
  confirm_password: "",
};

@Component
export default class Signup extends Vue {
  @CommonModule.Action(SIGNUP) [SIGNUP]: any;

  signupForm = JSON.parse(JSON.stringify(DEFAULT_SIGNUP_FORM));

  userSubmit(): void {
    const payload = { ...this.signupForm };
    delete payload.confirm_password;
    this[SIGNUP]({ payload })
      .then(() => {
        this.$router.push({ name: "Login" });
      })
      .catch((e: any) => {
        console.log(e);
        console.log(e.response);
      });
  }
}
</script>

<style scoped lang="scss">
.signup-container {
  margin-top: 10%;

  form {
    border: 1px solid;
    padding: 50px;
    border-radius: 2%;
  }
}
</style>
