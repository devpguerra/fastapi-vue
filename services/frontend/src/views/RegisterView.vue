<template>
  <section>
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" name="username" v-model="user.username" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="email" class="form-label">Email:</label>
        <input type="text" name="email" v-model="user.email" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="full_name" class="form-label">Full Name:</label>
        <input type="text" name="full_name" v-model="user.full_name" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="user.password" class="form-control" />
      </div>
      <button 
        type="submit" 
        class="btn btn-primary" 
        :disabled="!user.username || !user.email || !user.password"
      >
        Submit
      </button>
    </form>
  </section>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const user = reactive({
  username: '',
  full_name: '',
  email: '',
  password: '',
})

function isValidEmail(email) {
  const re = /\S+@\S+\.\S+/
  return re.test(email)
}

async function submit() {
  if (!user.username.trim()) {
    alert('Username is required')
    return
  }
  if (!user.email.trim() || !isValidEmail(user.email)) {
    alert('Valid email is required')
    return
  }
  if (!user.password) {
    alert('Password is required')
    return
  }
  try {
    await userStore.register(user)
    router.push('/dashboard')
  } catch (error) {
    alert('Username or email already exists. Please try again.')
  }
}
</script>
