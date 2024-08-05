import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import axiosInstance from './axiosInstance'
// import * as stream from "node:stream";

async function initApp() {
    const app = createApp(App);

    // app.provide('axios', axiosInstance);
    app.use(store);
    app.use(router);

    try {
        await store.dispatch('initializeAuth');
    } catch (error) {
        console.error('Failed to initialize authentication:', error);
    }

    app.mount("#app")
}

initApp();