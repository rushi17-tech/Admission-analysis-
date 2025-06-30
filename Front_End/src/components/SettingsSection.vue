<!-- src/components/Settings.vue -->
<script setup lang="ts">
import { useRouter } from 'vue-router'
const router = useRouter()
function logout () {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>

<template>
  <div class="relative py-10 px-3 md:px-10 min-h-[82vh] animate-fade-in text-white">
    <!-- heading -->
    <h3 class="page-heading mb-12 text-4xl font-extrabold tracking-wide">
      Settings
    </h3>

    <!-- panel -->
    <div class="glass-panel max-w-sm mx-auto p-8 rounded-2xl flex flex-col items-center gap-6">
      <button
        @click="logout"
        class="logout-btn w-full flex items-center justify-center gap-3"
      >
        <!-- animated logout icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
          <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
            <path stroke-dasharray="36" stroke-dashoffset="36" d="M12 4h-7c-.55 0-1 .45-1 1v14c0 .55.45 1 1 1h7">
              <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.5s" values="36;0"/>
            </path>
            <path stroke-dasharray="14" stroke-dashoffset="14" d="M9 12h11.5">
              <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.6s" dur="0.2s" values="14;0"/>
            </path>
            <path stroke-dasharray="6" stroke-dashoffset="6" d="M20.5 12l-3.5-3.5M20.5 12l-3.5 3.5">
              <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.8s" dur="0.2s" values="6;0"/>
            </path>
          </g>
        </svg>
        Logout
      </button>
    </div>
  </div>
</template>

<style scoped>
/* blurred heading strip */
.page-heading{
  @apply inline-block px-6 py-3 rounded-2xl;
  background: rgba(17,24,39,0.55);
  backdrop-filter: blur(14px) saturate(160%);
}

/* glass panel */
.glass-panel{
  background: rgba(17,24,39,0.55);
  backdrop-filter: blur(18px) saturate(160%);
  border: 1.5px solid rgba(255,255,255,0.12);
  box-shadow: 0 6px 32px rgba(74,222,255,.15),
              0 1.5px 8px rgba(139,92,246,.15);
}

/* logout button */
.logout-btn{
  @apply px-6 py-3 rounded-full font-semibold text-white shadow
          bg-gradient-to-r from-red-600 to-pink-600 transition;
}
.logout-btn:hover,
.logout-btn:focus{
  @apply from-pink-600 to-red-600 scale-105;
}

/* fade animation */
.fade-enter-active,.fade-leave-active{ transition:opacity .3s; }
.fade-enter-from,.fade-leave-to{ opacity:0; }
@keyframes fadeIn{ from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0);} }
.animate-fade-in{ animation:fadeIn .6s ease forwards; }
</style>
