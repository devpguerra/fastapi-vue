<template>
  <div class="error-message">
    <h2>Login Error</h2>
    <p>{{ message }}</p>
    <router-link to="/login">Go back to login</router-link>
  </div>
</template>

<script>
export default {
  computed: {
    message() {
      return this.$route.query.msg || "Something went wrong with the login process.";
    }
  }
}
</script>
