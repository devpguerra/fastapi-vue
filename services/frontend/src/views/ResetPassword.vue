<template>
  <div class="reset-password">
    <h2>Reset Your Password</h2>
    <form @submit.prevent="submitNewPassword">
      <div>
        <label>New Password</label>
        <input type="password" v-model="form.newPassword" required />
      </div>
      <button type="submit">Reset Password</button>
      <p v-if="message">{{ message }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const form = reactive({
  newPassword: '',
})

const message = ref('')

async function submitNewPassword() {
  try {
    const token = route.query.token
    if (!token) {
      message.value = 'Token is missing'
      return
    }
    const response = await axios.post('/reset-password', {
      token,
      new_password: form.newPassword,
    })
    message.value = response.data.message || 'Password successfully reset!'
    // Redirect to login after 3 seconds
    setTimeout(() => router.push('/login'), 3000)
  } catch (error) {
    message.value = error.response?.data?.detail || 'Something went wrong'
  }
}
</script>

<style scoped>
/* Add your styles here */
</style>
