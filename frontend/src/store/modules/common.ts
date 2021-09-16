// import axios from "axios";
import axios from "axios";
import { GetterTree, ActionTree, MutationTree, Module } from "vuex";

import {
  LOGIN,
  SIGNUP,
  LOGOUT,
  FETCH_PROFILE,
  UPDATE_PROFILE,
  CHANGE_PASSWORD,
  GET_TOKEN_FROM_LOCAL_STORE,
  FETCH_NOTES,
  FETCH_NOTE_DETAILS,
  CREATE_OR_UPDATE_NOTE,
  DELETE_NOTE,
  FETCH_SHARE_NOTES,
  FETCH_SHARE_NOTE_DETAILS,
} from "../action.names";
import {
  AUTHENTICATED,
  ACCESS_LEVEL,
  AUTH_HEADER,
  PROFILE,
} from "../getter.names";
import {
  SIGNUP_URL,
  LOGIN_URL,
  PROFILE_URL,
  CHANGE_PASSWORD_URL,
  NOTE_URL,
} from "../endpoints";
import { UserRoles } from "../../utils/permissions";
import { AxiosError } from "axios";
import {
  NOTE_DETAIL_URL,
  SHARE_NOTE_URL,
  SHARE_NOTE_DETAIL_URL,
} from "../endpoints";
import {
  SET_TOKEN,
  SET_TOKEN_ERROR,
  SET_PROFILE_DATA,
  CLEAR_PROFILE_DATA,
} from "../mutation.names";
import { buildParams } from "../utils";

const state: any = {
  user: {},
  token: null,
  error: {},
};

const getters: GetterTree<any, any> = {
  [AUTHENTICATED](state: any): boolean {
    if (state.token) return true;
    return false;
  },
  [ACCESS_LEVEL](state: any): number | null {
    return state.token ? UserRoles.PRIVATE : null;
  },
  [AUTH_HEADER](state): any {
    if (state.token == null) return {};
    return { Authorization: `Bearer ${state.token}` };
  },
  [PROFILE](state: any): number | null {
    return state.user;
  },
};

const actions: ActionTree<any, any> = {
  [GET_TOKEN_FROM_LOCAL_STORE]({ commit, dispatch }): Promise<any> {
    return new Promise((resolve, reject) => {
      const localToken = localStorage.getItem("TECHNOTE_TOKEN");
      if (localToken) {
        commit(SET_TOKEN, localToken);
        dispatch(FETCH_PROFILE)
          .then((data: any) => {
            resolve(data);
          })
          .catch((e: AxiosError) => {
            commit(CLEAR_PROFILE_DATA);
            reject(e);
          });
      } else {
        resolve({ message: "Token not exists" });
      }
    });
  },
  [SIGNUP](_, { payload }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .post(SIGNUP_URL, payload)
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [LOGIN]({ commit }, { payload }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .post(LOGIN_URL, payload)
        .then(({ data }) => {
          commit(SET_TOKEN, data.access);
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [LOGOUT]({ commit }): void {
    commit(CLEAR_PROFILE_DATA);
  },

  [FETCH_PROFILE]({ commit, getters }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .get(PROFILE_URL, {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          commit(SET_PROFILE_DATA, data);
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [UPDATE_PROFILE]({ getters }, { payload }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .patch(PROFILE_URL, payload, {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [CHANGE_PASSWORD]({ getters }, { payload }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .post(CHANGE_PASSWORD_URL, payload, {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },

  [CREATE_OR_UPDATE_NOTE]({ getters }, { payload, slug }): Promise<any> {
    return new Promise((resolve, reject) => {
      let method = axios.post;
      let url = NOTE_URL;
      if (slug) {
        method = axios.patch;
        url = NOTE_DETAIL_URL(slug);
      }
      method(url, payload, {
        headers: {
          ...getters[AUTH_HEADER],
        },
      })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [FETCH_NOTES]({ getters }, { filter }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .get(`${NOTE_URL}${buildParams(filter)}`, {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [FETCH_NOTE_DETAILS]({ getters }, { slug }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .get(NOTE_DETAIL_URL(slug), {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },

  [DELETE_NOTE]({ getters }, { slug }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .delete(NOTE_DETAIL_URL(slug), {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },

  [FETCH_SHARE_NOTES]({ getters }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .get(SHARE_NOTE_URL, {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
  [FETCH_SHARE_NOTE_DETAILS]({ getters }, { slug }): Promise<any> {
    return new Promise((resolve, reject) => {
      axios
        .get(SHARE_NOTE_DETAIL_URL(slug), {
          headers: {
            ...getters[AUTH_HEADER],
          },
        })
        .then(({ data }) => {
          resolve(data);
        })
        .catch((e: AxiosError) => {
          reject(e);
        });
    });
  },
};

const mutations: MutationTree<any> = {
  [SET_TOKEN](state, token) {
    state.token = token;
    state.error = false;
    localStorage.setItem("TECHNOTE_TOKEN", token);
  },
  [SET_PROFILE_DATA](state, data) {
    state.user = data;
  },
  [SET_TOKEN_ERROR](state) {
    state.token = null;
    state.user = null;
    state.error = true;
    localStorage.removeItem("TECHNOTE_TOKEN");
  },
  [CLEAR_PROFILE_DATA](state) {
    state.token = null;
    state.user = null;
    state.error = false;
    localStorage.removeItem("TECHNOTE_TOKEN");
  },
};

const commonDataStore: Module<any, any> = {
  namespaced: true,
  getters,
  actions,
  mutations,
  state,
};

export default commonDataStore;
