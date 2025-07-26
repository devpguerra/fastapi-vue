<template>
  <div>
    <h2>{{ message }}</h2>
  </div>
</template>
<script setup>
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const message = ref("Confirming...")

onMounted(async () => {
  const token = route.query.token
  try {
    const res = await axios.get(`/confirm-email?token=${token}`)
    message.value = res.data.message
    setTimeout(() => router.push('/login'), 3000)
  } catch (err) {
    message.value = "Invalid or expired token"
  }
})
</script>

