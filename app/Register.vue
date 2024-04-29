<template>
  <div class="register">
    <AppHeader></AppHeader>
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="formData.username" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="formData.password" required>
      </div>
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input type="text" id="firstName" v-model="formData.firstName" required>
      </div>
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input type="text" id="lastName" v-model="formData.lastName" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="formData.email" required>
      </div>
      <div class="form-group">
        <label for="location">Location</label>
        <input type="text" id="location" v-model="formData.location" required>
      </div>
      <div class="form-group">
        <label for="biography">Biography</label>
        <textarea id="biography" v-model="formData.biography" required></textarea>
      </div>
      <div class="form-group">
        <label for="profilePic">Profile Picture</label>
        <input type="file" id="profilePic" @change="handleFileUpload" accept="image/*" required>
      </div>
      <div class="form-group">
        <button type="submit">Register</button>
      </div>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    <p v-if="successMessage" class="success">{{ successMessage }}</p>
    <AppFooter></AppFooter>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import AppFooter from './AppFooter.vue';

export default {
  components: {
    AppHeader,
    AppFooter
  },
  data() {
    return {
      formData: {
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        email: '',
        location: '',
        biography: '',
        profilePic: null
      },
      errorMessage: '',
      successMessage: ''
    };
  },
  methods: {
    registerUser() {
      // Send registration data to backend API
      // You need to handle file upload differently depending on your backend setup
      // Example using Axios FormData:
      let formData = new FormData();
      formData.append('username', this.formData.username);
      formData.append('password', this.formData.password);
      formData.append('firstName', this.formData.firstName);
      formData.append('lastName', this.formData.lastName);
      formData.append('email', this.formData.email);
      formData.append('location', this.formData.location);
      formData.append('biography', this.formData.biography);
      formData.append('profilePic', this.formData.profilePic);
      
      axios.post('/api/v1/register', formData)
        .then(response => {
          this.successMessage = 'Registration successful!';
          // Optionally, redirect to login page or perform other actions
        })
        .catch(error => {
          this.errorMessage = 'Registration failed. Please try again.';
          console.error('Registration error:', error);
        });
    },
    handleFileUpload(event) {
      this.formData.profilePic = event.target.files[0];
    }
  }
};
</script>

<style scoped>
.register {
  max-width: 400px;
  margin: auto;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
}

input[type="text"],
input[type="password"],
input[type="email"],
textarea {
  width: 100%;
  padding: 0.5rem;
  font-size: 1rem;
}

button {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

.error {
  color: red;
}

.success {
  color: green;
}
</style>
