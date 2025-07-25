import 'bootstrap/dist/css/bootstrap.css';
import { createApp } from "vue";
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import axios from 'axios';

import App from './App.vue';
import router from './router';
import { useUserStore } from './stores/userStore';  // Import your Pinia user store

const app = createApp(App);

const pinia = createPinia();

pinia.use(piniaPluginPersistedstate)

app.use(pinia);
app.use(router);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://localhost:5000/';  // your FastAPI backend

// IMPORTANT: Pinia instance must be active before calling the store
// So we get userStore AFTER pinia is used in app

axios.interceptors.response.use(
  response => response,  // pass through success responses unchanged
  function (error) {
    if (error) {
      const originalRequest = error.config;
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        // Get userStore from pinia
        const userStore = useUserStore();

        userStore.logOut();

        router.push('/login');

        // Throw or reject to propagate the error
        return Promise.reject(error);
      }
    }

    // For all other errors, reject to propagate them
    return Promise.reject(error);
  }
);


app.mount("#app");
