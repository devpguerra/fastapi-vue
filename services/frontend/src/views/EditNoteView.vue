<template>
  <section>
    <h1>Edit note</h1>
    <hr/><br/>

    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="title" class="form-label">Title:</label>
        <input type="text" name="title" v-model="form.title" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">Content:</label>
        <textarea
          name="content"
          v-model="form.content"
          class="form-control"
        ></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { defineComponent, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useNotesStore } from '@/stores/notesStore'

export default defineComponent({
  name: 'EditNote',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const store = useNotesStore()

    const form = reactive({
      title: '',
      content: ''
    })

    const id = route.params.id

    // Load the note on mount
    onMounted(async () => {
      try {
        await store.viewNote(id)
        form.title = store.note?.title || ''
        form.content = store.note?.content || ''
      } catch (err) {
        console.error(err)
        router.push('/dashboard')
      }
    })

    async function submit() {
      try {
        await store.updateNote({ id, form })
        router.push({ name: 'Note', params: { id } })
      } catch (err) {
        console.error(err)
      }
    }

    return {
      form,
      submit
    }
  }
})
</script>
