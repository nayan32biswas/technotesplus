// import axios from "axios";
import { GetterTree, ActionTree, MutationTree, Module } from "vuex";

import { GET_TOKEN_FROM_LOCAL_STORE } from "../action.names";

const state: any = {};

const getters: GetterTree<any, any> = {};

const actions: ActionTree<any, any> = {
  async [GET_TOKEN_FROM_LOCAL_STORE](
    { commit, dispatch },
    accessLevel = null
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      resolve({});
    });
  },
};

const mutations: MutationTree<any> = {};

const commonDataStore: Module<any, any> = {
  namespaced: true,
  getters,
  actions,
  mutations,
  state,
};

export default commonDataStore;
