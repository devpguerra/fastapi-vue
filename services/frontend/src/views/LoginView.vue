<template>
  <section>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">Username or Email:</label>
        <input type="text" name="username" v-model="form.username" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="form.password" class="form-control" />
      </div>

      <div v-if="error" class="alert alert-danger">
        {{ error }}
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    <button @click="loginWithGoogle" class="btn-google">
      Login with Google
    </button>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';

export default defineComponent({
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      error: null,
    };
  },
  setup() {
    const router = useRouter();
    const userStore = useUserStore();

    return { router, userStore };
  },
  methods: {
    async submit() {
      this.error = null;
      const User = new FormData();
      //This could conatain email or username
      User.append('username', this.form.username);
      User.append('password', this.form.password);

      try {
        const success = await this.userStore.logIn(User);
        if (success) {
          this.router.push('/dashboard');
        } else {
          this.error = 'Invalid username or password';
        }
      } catch (e) {
        this.error = 'Login failed: ' + (e.message || e);
      }
    },
    loginWithGoogle() {
      const baseUrl = process.env.VUE_APP_API_BASE_URL;
      // Redirect the user to your backend Google OAuth route
      window.location.href = `${baseUrl}/login/google`;
  }
  },
});
</script>