<template>
  <div class="login-page">
    <h1>Login</h1>

    <form @submit.prevent="handleLogin" class="form">
      <div class="form-group">
        <label>Email</label>
        <input type="email" v-model="email" required />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input type="password" v-model="password" required />
      </div>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>

</script>

<style scoped>
.login-page {
  padding: 2rem;
  max-width: 400px;
  margin: auto;
  font-family: Arial, sans-serif;
  border: 2px solid #ddd;
  border-radius: 10px;
}

.form-group {
  margin-bottom: 1rem;
}

label {
  display: block;
  margin-bottom: 0.3rem;
}

input {
  width: 100%;
  padding: 0.5rem;
  box-sizing: border-box;
}

button {
  padding: 0.6rem 1.2rem;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  margin-top: 1rem;
  width: 100%;
  border-radius: 5px;
}

button:hover {
  background-color: #0069d9;
}

.error {
  color: red;
  margin-top: 0.5rem;
}
</style>
