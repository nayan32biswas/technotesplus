<template>
  <div v-if="profile" class="container">
    <div v-if="editProfile === false">
      <b-row>
        <b-col>Email: {{ profile.email }}</b-col>
        <b-col>Username: {{ profile.username }}</b-col>
      </b-row>
      <b-row>
        <b-col>Full name: {{ profile.first_name + profile.last_name }}</b-col>
      </b-row>
      <b-button @click.prevent="editProfile = true">Edit</b-button>
    </div>
    <div v-else>
      <ValidationObserver v-slot="{ handleSubmit }">
        <b-form @submit.prevent="handleSubmit(profileSubmit)">
          <b-row>
            <b-col>
              <ValidationProvider v-slot="{ errors, touched }" rules="required">
                <div>
                  <label>Email</label>
                  <input
                    type="text"
                    placeholder="Enter Email"
                    name="Email"
                    v-model="userForm.email"
                  />
                </div>
                <span v-if="touched && errors.length > 0" class="text-danger">{{
                  errors[0]
                }}</span>
              </ValidationProvider>
            </b-col>
            <b-col>
              <ValidationProvider v-slot="{ errors, touched }" rules="required">
                <div>
                  <label>Username</label>
                  <input
                    type="text"
                    placeholder="Enter Username"
                    name="Username"
                    v-model="userForm.username"
                  />
                </div>
                <span v-if="touched && errors.length > 0" class="text-danger">{{
                  errors[0]
                }}</span>
              </ValidationProvider>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <ValidationProvider v-slot="{ errors, touched }" rules="required">
                <div>
                  <label>First Name</label>
                  <input
                    type="text"
                    placeholder="Enter First Name"
                    name="Last Name"
                    v-model="userForm.first_name"
                  />
                </div>
                <span v-if="touched && errors.length > 0" class="text-danger">{{
                  errors[0]
                }}</span>
              </ValidationProvider>
            </b-col>
            <b-col>
              <ValidationProvider v-slot="{ errors, touched }" rules="required">
                <div>
                  <label>Last Name</label>
                  <input
                    type="text"
                    placeholder="Enter Last Name"
                    name="Last Name"
                    v-model="userForm.last_name"
                  />
                </div>
                <span v-if="touched && errors.length > 0" class="text-danger">{{
                  errors[0]
                }}</span>
              </ValidationProvider>
            </b-col>
          </b-row>
          <div>
            <button @click="editProfile = false">Cancel</button>
            <button type="submit">Save</button>
          </div>
        </b-form>
      </ValidationObserver>
    </div>
    <div v-if="passwordReset">
      <ValidationObserver v-slot="{ handleSubmit }">
        <b-form @submit.prevent="handleSubmit(passwordResetSubmit)">
          <ValidationProvider
            v-slot="{ errors, touched }"
            rules="required"
            vid="confirm_password"
          >
            <div>
              <label>Current Password</label>
              <input
                type="password"
                placeholder="Enter Current Password"
                name="Current Password"
                v-model="passwordResetForm.current_password"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </ValidationProvider>
          <ValidationProvider
            v-slot="{ errors, touched }"
            rules="required|min:8"
            vid="confirm_password"
          >
            <div>
              <label>New Password</label>
              <input
                type="password"
                placeholder="Enter New Password"
                name="New Password"
                v-model="passwordResetForm.new_password"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </ValidationProvider>

          <ValidationProvider
            v-slot="{ errors, touched }"
            rules="required|confirmed:confirm_password"
            vid="password2"
          >
            <div>
              <label>Confirm New Password</label>
              <input
                type="password"
                placeholder="Enter Confirm New Password"
                name="Confirm New Password"
                v-model="passwordResetForm.confirm_password"
              />
            </div>
            <span v-if="touched && errors.length > 0" class="text-danger">{{
              errors[0]
            }}</span>
          </ValidationProvider>

          <div>
            <button @click="passwordReset = false">Cancel</button>
            <b-button type="submit"> Reset Password </b-button>
          </div>
        </b-form>
      </ValidationObserver>
    </div>
    <div v-else>
      <b-button @click.prevent="passwordReset = true">Reset Password</b-button>
    </div>
  </div>
</template>

<script lang="ts">
import { CHANGE_PASSWORD, UPDATE_PROFILE } from "@/store/action.names";
import { PROFILE } from "@/store/getter.names";
import { CommonModule } from "@/store/namespace.names";
import { AxiosError } from "axios";
import { Component, Vue } from "vue-property-decorator";
import { ErrorHandler } from "vue-router/types/router";
const DEFAULT_USER_FORM = {
  email: "",
  username: "",
  first_name: "",
  last_name: "",
};
const DEFAULT_PASSWORD_RESET_FORM = {
  current_password: "",
  new_password: "",
  confirm_password: "",
};
@Component
export default class Profile extends Vue {
  @CommonModule.Getter(PROFILE) profile: any;
  @CommonModule.Action [UPDATE_PROFILE]: any;
  @CommonModule.Action [CHANGE_PASSWORD]: any;

  userForm = JSON.parse(JSON.stringify(DEFAULT_USER_FORM));
  passwordResetForm = JSON.parse(JSON.stringify(DEFAULT_PASSWORD_RESET_FORM));
  editProfile = false;
  passwordReset = false;

  profileSubmit(): void {
    const payload = { ...this.userForm };
    this[UPDATE_PROFILE]({ payload })
      .then(() => {
        this.editProfile = false;
        alert("Profile Updated");
      })
      .catch((e: any) => {
        console.log(e);
      });
  }
  passwordResetSubmit(): void {
    const payload = { ...this.passwordResetForm };
    this[CHANGE_PASSWORD]({ payload })
      .then(() => {
        alert("Password Changed.");
        this.passwordReset = false;
        this.passwordResetForm = JSON.parse(
          JSON.stringify(DEFAULT_PASSWORD_RESET_FORM)
        );
      })
      .catch((e: AxiosError) => {
        if (e?.response?.status) {
          alert("Incorrect Password. Try Again.");
        } else {
          alert("Something worng check debug.");
        }
      });
  }

  mounted(): void {
    if (this.profile) {
      this.userForm = { ...this.profile };
    }
  }
}
</script>

<style scoped lang="scss"></style>
