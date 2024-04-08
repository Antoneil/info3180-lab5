<template>
  <div>
    <!-- Error message -->
    <div v-if="state.errorMessage" class="error-message">{{ state.errorMessage }}</div>

    <form @submit.prevent="saveMovie" id="movieForm">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" v-model="formData.title" name="title" class="form-control" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea v-model="formData.description" name="description" class="form-control"></textarea>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" @change="onFileChange" name="poster" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>

    <!-- Success message -->
    <div v-if="state.successMessage" class="success-message">{{ state.successMessage }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const formData = ref({
  title: '',
  description: '',
  poster: null
});

const state = ref({
  successMessage: '',
  errorMessage: ''
});

async function saveMovie() {
  try {
    const form_data = new FormData(document.getElementById('movieForm'));
    const response = await fetch("/api/v1/movies", {
      method: 'POST',
      body: form_data,
      headers: {
        'X-CSRFToken': csrf_token.value
      }
    });
    const data = await response.json();
    if (data.success) {
      state.successMessage = data.message;
      // Clear form data on success
      formData.title = '';
      formData.description = '';
      formData.poster = null;
    } else {
      state.errorMessage = data.message;
    }
  } catch (error) {
    state.errorMessage = 'An error occurred while submitting the form.';
    console.log(error);
  }
}

const csrf_token = ref('');

async function getCsrfToken() {
  try {
    const response = await fetch('/api/v1/csrf-token');
    const data = await response.json();
    csrf_token.value = data.csrf_token;
  } catch (error) {
    console.log(error);
  }
}

getCsrfToken();

function onFileChange(event) {
  formData.poster = event.target.files[0];
}
</script>
