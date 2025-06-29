<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
function logout () { localStorage.removeItem('token'); router.push('/login') }
</script>

<template>
  <div class="p-6">
    <h3 class="text-2xl font-bold mb-6 text-gray-800">Settings</h3>
    <div class="bg-white rounded-xl shadow-md p-6 max-w-sm">
      <button
        @click="logout"
        class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700
               text-white font-semibold rounded-lg transition"
      >
        🔒 Logout
      </button>
    </div>
  </div>
</template>
