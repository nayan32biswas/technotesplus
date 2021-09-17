import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";

import { UserRoles } from "@/utils/permissions";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
    meta: {
      accessLevel: null,
    },
  },
  {
    path: "/signup",
    name: "Signup",
    component: () => import("../views/Signup.vue"),
    meta: {
      accessLevel: null,
    },
  },
  {
    path: "/profile/",
    name: "Profile",
    component: () => import("../views/Profile.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "/note/create",
    name: "NoteCreate",
    component: () => import("../views/NoteCreate.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "/note/:slug",
    name: "NoteDetails",
    component: () => import("../views/NoteDetails.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "/shared-note",
    name: "ShareWithMeNote",
    component: () => import("../views/ShareWithMeNote.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "/shared-note/:slug",
    name: "ShareWithMeNoteDetails",
    component: () => import("../views/ShareWithMeNoteDetails.vue"),
    meta: {
      accessLevel: UserRoles.PRIVATE,
    },
  },
  {
    path: "*",
    name: "404",
    component: () => import("../views/404.vue"),
    meta: {
      accessLevel: null,
    },
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
