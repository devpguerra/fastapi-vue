<template>
  <div class="forgot-password">
    <h2>Forgot Password</h2>
    <form @submit.prevent="submitEmail">
      <div>
        <label>Email Address</label>
        <input type="email" v-model="form.email" required />
      </div>
      <button type="submit">Send Reset Link</button>
      <p v-if="message">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

const form = reactive({
  email: '',
})

const message = ref('')

async function submitEmail() {
  try {
    const response = await axios.post('/forgot-password', {
      email: form.email,
    })
    message.value = response.data.message || 'If your email is registered, you will receive a reset link.'
  } catch (error) {
    message.value = error.response?.data?.detail || 'Something went wrong'
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>
