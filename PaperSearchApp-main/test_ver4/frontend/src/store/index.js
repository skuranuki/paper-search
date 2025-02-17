import { createStore } from "vuex";

export default createStore({
  state: {
    clicks: [],
  },
  mutations: {
    logClick(state, click) {
      state.clicks.push(click);
    },
  },
  actions: {
    logClick({ commit }, click) {
      commit("logClick", click);
    },
  },
  getters: {
    getLogClick: (state) => state.clicks,
  },
});
