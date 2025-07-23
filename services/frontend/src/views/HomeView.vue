<template>
  <section>
    <p>This site is built with FastAPI and Vue.</p>

    <div v-if="isLoggedIn" id="logout">
      <span>Click <router-link to="/dashboard">here</router-link> to view all notes.</span>
    </div>
    <p v-else>
      <span><router-link to="/register">Register</router-link></span>
      <span> or </span>
      <span><router-link to="/login">Log In</router-link></span>
    </p>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { useUserStore } from '@/stores/userStore';

export default defineComponent({
  name: 'HomeView',
  setup() {
    const userStore = useUserStore();

    return {
      isLoggedIn: userStore.isAuthenticated,
    };
  },
});
</script>
