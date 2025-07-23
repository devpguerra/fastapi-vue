import { defineStore } from 'pinia'
import axios from 'axios'

export const useNotesStore = defineStore('note', {
  state: () => ({
    notes: [],
    note: null,
  }),

  getters: {
    stateNotes: (state) => state.notes,
    stateNote: (state) => state.note,
  },

  actions: {
    async createNote(note) {
      await axios.post('notes', note)
      await this.getNotes()
    },

    async getNotes() {
      try {
        const { data } = await axios.get('notes')
        this.notes = data
      } catch (error) {
        console.error('Failed to get notes', error)
      }
    },

    async viewNote(id) {
      try {
        const { data } = await axios.get(`note/${id}`)
        this.note = data
      } catch (error) {
        console.error('Failed to get note', error)
      }
    },

    async updateNote(note) {
      try {
        await axios.patch(`note/${note.id}`, note.form)
      } catch (error) {
        console.error('Failed to update note', error)
      }
    },

    async deleteNote(id) {
      try {
        await axios.delete(`note/${id}`)
      } catch (error) {
        console.error('Failed to delete note', error)
      }
    },
  },
})