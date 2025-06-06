<template>
  <div class="signup-page">
    <div class="overlay"></div>
    
    <div class="signup-card">
      <h1>Signup Page</h1>
      <p class="subtitle">Create your account below</p>

      <form @submit.prevent="handleSignup" class="form">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" required class="animated-input" />
        </div>

        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required class="animated-input" />
        </div>

        <div class="form-group">
          <label>Confirm Password</label>
          <input type="password" v-model="confirmPassword" required class="animated-input" />
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button type="submit" class="ripple-button">Signup</button>
        <a href="/login" class="nav-button">Already have an account?Login</a>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')

const handleSignup = () => {
  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match!'
  } else {
    errorMessage.value = ''
    // Signup logic here
    alert('Signup successful!')
  }
}
</script>

<style scoped>
.signup-page {
   position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  background: url('/admission-bg.png') no-repeat center center;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
  z-index: 0;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 50, 0.3);
  z-index: 1;
}

.signup-card {
  position: relative;
  z-index: 2;
  background: rgba(255, 255, 255, 0.95);
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 400px;
  text-align: center;
  animation: card-pop 1s ease forwards;
  transition: transform 0.3s ease;
}

.signup-card:hover {
  transform: translateY(-5px) scale(1.02);
}

h1, .subtitle {
  animation: slide-down 0.6s ease;
}

.subtitle {
  font-size: 0.95rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
  text-align: left;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.4rem;
  color: #333;
}

input.animated-input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

input.animated-input:hover,
input.animated-input:focus {
  transform: translateY(-3px);
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.4);
  border-color: #007bff;
  outline: none;
}

button.ripple-button {
  width: 100%;
  padding: 0.7rem;
  font-size: 1rem;
  background-color: #007bff;
  border: none;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

button.ripple-button:hover {
  transform: translateY(-3px) scale(1.05);
  background-color: #0056b3;
}

button.ripple-button::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.4);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.5s ease, height 0.5s ease;
}

button.ripple-button:active::after {
  width: 200%;
  height: 500%;
}

.error {
  color: red;
  font-size: 0.9rem;
  margin-top: 0.5rem;
  animation: fade-in 0.5s ease;
}

/* Animations */
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slide-down {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes card-pop {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>
