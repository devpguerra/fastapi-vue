<template>
  <section>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
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
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password:'',
      },
      error: null,
    };
  },
  methods: {
    ...mapActions(['logIn']),
    async submit() {
      this.error = null;
      const User = new FormData();
      User.append('username', this.form.username);
      User.append('password', this.form.password);
      
      try {
        const success = await this.logIn(User);
        if (success) {
          this.$router.push('/dashboard');
        } else {
          this.error = 'Invalid username or password';
        }
      } catch (e) {
        this.error = 'Login failed: ' + (e.message || e);
      }
    }
  }
});
</script>