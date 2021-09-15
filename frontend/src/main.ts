import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

import { namespaced } from "./store/utils";
import { NS_COMMON } from "./store/namespace.names";
import { GET_TOKEN_FROM_LOCAL_STORE } from "./store/action.names";
import { ACCESS_LEVEL } from "./store/getter.names";

function checkAuth(to: any, from: any, next: any) {
  const accessLevel = store.getters[namespaced(NS_COMMON, ACCESS_LEVEL)];
  if (to.meta?.accessLevel !== null) {
    if (accessLevel !== null) {
      if (to.meta?.accessLevel <= accessLevel) {
        next();
      } else {
        next("/");
      }
    } else {
      next("/login");
    }
  } else {
    next();
  }
}

router.beforeEach((to: any, from: any, next: any) => {
  if (from === null || from.name === null) {
    store
      .dispatch(
        namespaced(NS_COMMON, GET_TOKEN_FROM_LOCAL_STORE),
        to.meta?.accessLevel
      )
      .then(() => {
        checkAuth(to, from, next);
      })
      .catch(() => {
        checkAuth(to, from, next);
      });
  } else {
    checkAuth(to, from, next);
  }
});

Vue.config.productionTip = false;

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
