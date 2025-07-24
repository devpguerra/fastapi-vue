<template>
  <div>
    <section>
      <h1>Add new note</h1>
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

    <br/><br/>

    <section>
      <h1>Notes</h1>
      <hr/><br/>

      <div v-if="notes && notes.length">
        <div v-for="note in notes" :key="note.id" class="notes">
          <div class="card" style="width: 18rem;">
            <div class="card-body">
              <ul>
                <li><strong>Note Title:</strong> {{ note.title }}</li>
                <li><strong>Author:</strong> {{ note.author.username }}</li>
                <li><router-link :to="{name: 'Note', params:{id: note.id}}">View</router-link></li>
              </ul>
            </div>
          </div>
          <br/>
        </div>
      </div>

      <div v-else>
        <p>Nothing to see. Check back later.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent, reactive, onMounted, toRefs, computed  } from 'vue'
import { useNotesStore } from '@/stores/notesStore'

export default defineComponent({
  name: 'Dashboard',
  setup() {
    const notesStore = useNotesStore()
    
    //reactive form state
    const form = reactive({
      title: '',
      content: '',
    })

    const notes = computed(() => notesStore.notes)
    // fetch notes on mount
    onMounted(() => {
      notesStore.getNotes()
    })

    async function submit() {
      await notesStore.createNote(form)
      // clear form after submit if needed
      form.title = ''
      form.content = ''
    }

    return {
      form,
      notes,
      submit,
    }
  }
})
</script>
