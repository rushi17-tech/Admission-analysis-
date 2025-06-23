<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

const emit = defineEmits(['login-success'])

const handleLogin = () => {
  if (email.value === 'welcome@gmail.com' && password.value === '1234') {
    emit('login-success')
    router.push('/home')
  } else {
    errorMessage.value = 'Invalid email or password. Please try again.'
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="user-box">
          <input type="email" v-model="email" required />
          <label>Email</label>
        </div>
        <div class="user-box">
          <input type="password" v-model="password" required />
          <label>Password</label>
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <button class="neon-button" type="submit">
          <span></span><span></span><span></span><span></span>
          Submit
        </button>
        <p class="signup-link">
          Don't have an account?
          <router-link to="/signup">Signup here</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  height: 100vh;
  margin: 0;
  padding: 0;
  font-family: sans-serif;
  background: linear-gradient(#141e30, #243b55);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-box {
  background: rgba(0, 0, 0, 0.5);
  padding: 40px;
  width: 400px;
  border-radius: 10px;
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.6);
  box-sizing: border-box;
  text-align: center;
}

.login-box h2 {
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

.signup-link {
  margin-top: 20px;
  color: #ccc;
}
.signup-link a {
  color: #03e9f4;
  text-decoration: underline;
}
.signup-link a:hover {
  color: #fff;
}
</style>
