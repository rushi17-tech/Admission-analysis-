<template>
  <div class="signup-page">
    <div class="signup-box">
      <h2>Signup</h2>
      <form @submit.prevent="handleSignup">
        <div class="user-box">
          <input type="email" v-model="email" required />
          <label>Email</label>
        </div>
        <div class="user-box">
          <input type="password" v-model="password" required />
          <label>Password</label>
        </div>
        <div class="user-box">
          <input type="password" v-model="confirmPassword" required />
          <label>Confirm Password</label>
        </div>

        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="neon-button" type="submit">
          <span></span><span></span><span></span><span></span>
          Signup
        </button>

        <p class="login-link">
          Already have an account?
          <router-link to="/login">Login here</router-link>
        </p>
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
    alert('Signup successful!')
  }
}
</script>

<style scoped>
.signup-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: linear-gradient(#141e30, #243b55);
  display: flex;
  align-items: center;
  justify-content: center;
}

.signup-box {
  background: rgba(0, 0, 0, 0.5);
  padding: 40px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.6);
  box-sizing: border-box;
  text-align: center;
}

.signup-box h2 {
  color: #fff;
  margin-bottom: 30px;
}

.user-box {
  position: relative;
  margin-bottom: 30px;
}

.user-box input {
  width: 100%;
  padding: 10px 0;
  background: transparent;
  border: none;
  border-bottom: 1px solid #fff;
  color: #fff;
  font-size: 16px;
  outline: none;
}

.user-box label {
  position: absolute;
  top: 0;
  left: 0;
  padding: 10px 0;
  font-size: 16px;
  color: #fff;
  pointer-events: none;
  transition: 0.5s;
}

.user-box input:focus ~ label,
.user-box input:valid ~ label {
  top: -20px;
  font-size: 12px;
  color: #03e9f4;
}

.neon-button {
  position: relative;
  display: inline-block;
  padding: 10px 20px;
  color: #03e9f4;
  font-size: 16px;
  background: none;
  border: none;
  cursor: pointer;
  text-transform: uppercase;
  overflow: hidden;
  margin-top: 20px;
  letter-spacing: 4px;
}

.neon-button:hover {
  background: #03e9f4;
  color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 5px #03e9f4,
              0 0 25px #03e9f4,
              0 0 50px #03e9f4,
              0 0 100px #03e9f4;
}

.neon-button span {
  position: absolute;
  display: block;
}

.neon-button span:nth-child(1) {
  top: 0;
  left: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #03e9f4);
  animation: anim1 1s linear infinite;
}

.neon-button span:nth-child(2) {
  right: 0;
  top: -100%;
  width: 2px;
  height: 100%;
  background: linear-gradient(180deg, transparent, #03e9f4);
  animation: anim2 1s linear infinite;
  animation-delay: 0.25s;
}

.neon-button span:nth-child(3) {
  bottom: 0;
  right: -100%;
  width: 100%;
  height: 2px;
  background: linear-gradient(270deg, transparent, #03e9f4);
  animation: anim3 1s linear infinite;
  animation-delay: 0.5s;
}

.neon-button span:nth-child(4) {
  left: 0;
  bottom: -100%;
  width: 2px;
  height: 100%;
  background: linear-gradient(360deg, transparent, #03e9f4);
  animation: anim4 1s linear infinite;
  animation-delay: 0.75s;
}

@keyframes anim1 {
  0% { left: -100%; }
  50%, 100% { left: 100%; }
}
@keyframes anim2 {
  0% { top: -100%; }
  50%, 100% { top: 100%; }
}
@keyframes anim3 {
  0% { right: -100%; }
  50%, 100% { right: 100%; }
}
@keyframes anim4 {
  0% { bottom: -100%; }
  50%, 100% { bottom: 100%; }
}

.error {
  color: #ff4d4f;
  margin-top: -10px;
  font-size: 0.9rem;
}

.login-link {
  margin-top: 20px;
  color: #ccc;
}
.login-link a {
  color: #03e9f4;
  text-decoration: underline;
}
.login-link a:hover {
  color: #fff;
}
</style>
