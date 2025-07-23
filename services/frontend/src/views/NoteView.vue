<template>
  <div v-if="note">
    <p><strong>Title:</strong> {{ note.title }}</p>
    <p><strong>Content:</strong> {{ note.content }}</p>
    <p><strong>Author:</strong> {{ note.author.username }}</p>

    <div v-if="user && note.author && user.id === note.author.id">
      <p>
        <router-link
          :to="{ name: 'EditNote', params: { id: note.id } }"
          class="btn btn-primary"
        >Edit</router-link>
      </p>
      <p>
        <button @click="removeNote" class="btn btn-danger">Delete</button>
      </p>
    </div>
  </div>
</template>

<script>
import { defineComponent, onMounted, computed } from 'vue'
import { useNotesStore } from '@/stores/notesStore'
import { useUserStore } from '@/stores/userStore'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'Note',
  props: ['id'],
  setup(props, { emit, expose }) {
    const notesStore = useNotesStore()
    const userStore = useUserStore()

    const note = computed(() => notesStore.note)
    const user = computed(() => userStore.user)

    const route = useRoute()
    const router = useRouter()

    const loadNote = async () => {
      try {
        await notesStore.viewNote(props.id)
      } catch (error) {
        console.error(error)
        // Redirect on error
        router.push('/dashboard')
      }
    }

    const removeNote = async () => {
      try {
        await notesStore.deleteNote(props.id)
        router.push('/dashboard')
      } catch (error) {
        console.error(error)
      }
    }

    onMounted(() => {
      loadNote()
    })

    return {
      note,
      user,
      removeNote,
    }
  },
})
</script>
