<template>
  <div>
    <div
      class="d-flex align-items-center justify-content-center login-container"
    >
      <ValidationObserver v-slot="{ handleSubmit }">
        <b-form @submit.prevent="handleSubmit(loginSubmit)">
          <ValidationProvider v-slot="{ errors, touched }" rules="required">
            <div>
              <label>Username</label>
              <div>
                <input
                  type="text"
                  placeholder="Enter Username"
                  name="Username"
                  v-model="loginForm.username"
                />
              </div>
              <span v-if="touched && errors.length > 0" class="text-danger">{{
                errors[0]
              }}</span>
            </div>
          </ValidationProvider>

          <ValidationProvider v-slot="{ errors, touched }" rules="required">
            <div class="mt-2">
              <label>Password</label>
              <div>
                <input
                  type="password"
                  placeholder="Enter Password"
                  name="Password"
                  v-model="loginForm.password"
                />
              </div>
              <span v-if="touched && errors.length > 0" class="text-danger">{{
                errors[0]
              }}</span>
            </div>
          </ValidationProvider>

          <div v-if="loginErrorMessage" class="text-danger">
            {{ loginErrorMessage }}
          </div>

          <div class="mt-3">
            <b-button type="submit">Login</b-button>
          </div>
        </b-form>
      </ValidationObserver>
      <router-link :to="{ name: 'Signup' }">Signup</router-link>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import { LOGIN } from "@/store/action.names";
import { CommonModule } from "@/store/namespace.names";
import { AxiosError } from "axios";

const DEFAULT_LOGIN_FORM = {
  username: "",
  password: "",
};

@Component
export default class Login extends Vue {
  @CommonModule.Action(LOGIN) [LOGIN]: any;

  loginForm = JSON.parse(JSON.stringify(DEFAULT_LOGIN_FORM));
  loginErrorMessage = "";

  loginSubmit(): void {
    const payload = { ...this.loginForm };
    this[LOGIN]({ payload })
      .then(() => {
        this.$router.push({ name: "Home" });
      })
      .catch((e: AxiosError) => {
        console.log(e);
      });
  }
}
</script>

<style scoped lang="scss">
.login-container {
  margin-top: 10%;

  form {
    border: 1px solid;
    padding: 50px;
    border-radius: 2%;
  }
}
</style>
