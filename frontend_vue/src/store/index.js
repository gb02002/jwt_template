import { createStore } from 'vuex'
import AuthService from '@/services/AuthService'


export default createStore({
  state: {
    isAuthenticated: false,
    // token: localStorage.getItem('token') || null,
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
  },
  mutations: {
    setAuthenticated(state, payload) {
      state.isAuthenticated = payload;
    }
  },
  actions: {
    async initializeAuth({ commit }) {
      return new Promise((resolve, reject) => {
        const token = localStorage.getItem("token");
        if (token) {
          // Assuming the token is valid for simplicity. You might want to validate it here.
          commit('setAuthenticated', true);
          resolve();
        } else {
          commit('setAuthenticated', false);
          resolve();
        }
      });
    },
    async login({ commit }, {username, password}) {
      try {
        const response = await AuthService.login(username, password)
        if (response && response.status === 202) {            
          localStorage.setItem("token", response.data);
          commit('setAuthenticated', true);
        } else {
          commit('setAuthenticated', false);
        }
      } catch (error) {
        console.error(error);
      }
    },
    async logout({ commit }) {
      try {
        const response = await AuthService.logout();
        if (response.status === 202) {
          // Удаление токена из localStorage
          localStorage.removeItem("token");
          // Обновление состояния аутентификации
          commit('setAuthenticated', false);
        } else {
          // Логирование ошибки в случае неуспешного ответа
          console.error(`Logout failed with status: ${response.status}`);
        }
      } catch (error) {
        console.error(error);
      }
    },
    async register({ commit }, username, password) {
      try {
        await AuthService.register(username, password);
      } catch (error) {
        console.error(error);
      }
    },
    async refreshToken({ commit }) {
      try {
        const response = await AuthService.refreshToken();
        localStorage.setItem("token", response.data);
        commit('setAuthenticated', true);
      } catch (error) {
        console.error("Failed to refresh token:", error);
        commit('setAuthenticated', false);
      }
    },
  },
  modules: {},
});
