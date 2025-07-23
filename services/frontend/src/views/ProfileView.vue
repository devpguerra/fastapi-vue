<template>
  <section>
    <h1>Your Profile</h1>
    <hr /><br />
    <div>
      <div v-if="user">
        <p><strong>Full Name:</strong> <span>{{ user.full_name }}</span></p>
        <p><strong>Username:</strong> <span>{{ user.username }}</span></p>
        <p>
          <button @click="deleteAccount" class="btn btn-primary">Delete Account</button>
        </p>
      </div>
    </div>
  </section>
</template>

<script>
import { defineComponent, onMounted, computed } from 'vue'
import { useUserStore } from '@/stores/userStore';

export default defineComponent({
  name: 'Profile',
  setup() {
    const userStore = useUserStore()

    const user = computed(() => userStore.user)

    const deleteAccount = async () => {
      try {
        await userStore.deleteUser(user.value.id)
        await userStore.logOut()
        window.location.href = '/'
      } catch (error) {
        console.error(error)
      }
    }

    onMounted(() => {
      userStore.viewMe()
    })

    return {
      user,
      deleteAccount,
    }
  },
})
</script>