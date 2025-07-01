<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuViewport
} from '@/components/ui/navigation-menu'
import { BarChart, Users, FilePlus2, CalendarDays } from 'lucide-vue-next'

import HomeSection         from '@/components/HomeSection.vue'
import StudentsSection     from '@/components/StudentsSection.vue'
import ApplicationsSection from '@/components/ApplicationsSection.vue'
import ScheduleSection     from '@/components/ScheduleSection.vue'
import AnalyticsSection    from '@/components/AnalyticsSection.vue'
import SettingsSection     from '@/components/SettingsSection.vue'


const activeTab = ref<
  'home' | 'students' | 'applications' | 'schedule' | 'analytics' | 'settings'
>('home')

// Rare: Dynamically generated grid for background
onMounted(() => {
  if (typeof window !== 'undefined') {
    const gridBg = document.getElementById('dynamic-grid-bg')
    if (gridBg) {
      const w = window.innerWidth
      const h = window.innerHeight
      const cols = Math.floor(w / 60)
      const rows = Math.floor(h / 60)
      gridBg.innerHTML = ''
      for (let i = 0; i < cols * rows; i++) {
        const cell = document.createElement('div')
        cell.className = 'grid-cell'
        gridBg.appendChild(cell)
      }
    }
  }

  if (!document.querySelector('script[data-dotlottie-player]')) {
    const script = document.createElement('script')
    script.type = 'module'
    script.src =
      'https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs'
    script.setAttribute('data-dotlottie-player', 'true')
    document.head.appendChild(script)
  }
})
</script>

<template>
  <!-- Rare: Dynamic Grid Background (JS-generated) -->
  <div id="dynamic-grid-bg" class="fixed inset-0 z-0 pointer-events-none grid grid-flow-col auto-cols-[60px] auto-rows-[60px] opacity-15"></div>

  <!-- Rare: Morphing SVG Path -->
  <div class="fixed inset-0 z-0 pointer-events-none">
    <svg class="w-full h-full" viewBox="0 0 1920 1080" preserveAspectRatio="none">
      <path id="morph-shape" d="M300,200 L800,200 L800,600 L300,600 Z" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-opacity="0.3">
        <animate attributeName="d"
                 values="M300,200 L800,200 L800,600 L300,600 Z;
                         M400,100 L900,100 L900,700 L400,700 Z;
                         M200,300 L700,300 L700,500 L200,500 Z;
                         M300,200 L800,200 L800,600 L300,600 Z"
                 dur="30s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform"
                          attributeType="XML"
                          type="rotate"
                          values="0 550 400; 10 550 400; -10 550 400; 0 550 400"
                          dur="25s"
                          repeatCount="indefinite"/>
      </path>
      <path d="M1200,300 L1700,300 L1700,800 L1200,800 Z" fill="none" stroke="#a21caf" stroke-width="1.5" stroke-opacity="0.3" transform="translate(0,0)">
        <animate attributeName="d"
                 values="M1200,300 L1700,300 L1700,800 L1200,800 Z;
                         M1300,200 L1800,200 L1800,900 L1300,900 Z;
                         M1100,400 L1600,400 L1600,700 L1100,700 Z;
                         M1200,300 L1700,300 L1700,800 L1200,800 Z"
                 dur="35s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform"
                          attributeType="XML"
                          type="rotate"
                          values="0 1450 550; 5 1450 550; -5 1450 550; 0 1450 550"
                          dur="27s"
                          repeatCount="indefinite"/>
      </path>
    </svg>
  </div>

  <!-- Navigation Bar -->
  <div class="relative z-10 w-full bg-[#1f2937]/95 p-4 shadow-lg backdrop-blur-lg border-b border-[#3b82f6]/30 animate-fade-in">
    <NavigationMenu class="w-full">
      <NavigationMenuList class="flex space-x-4">
        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'home'" class="menu-item flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" viewBox="0 0 24 24">
              <g fill="none" stroke="#fefefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8">
                <path stroke-dasharray="16" stroke-dashoffset="16" d="M4.5 21.5h15">
                  <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.8s" values="16;0" />
                </path>
                <path stroke-dasharray="16" stroke-dashoffset="16" d="M4.5 21.5v-13.5M19.5 21.5v-13.5">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.8s" dur="0.8s" values="16;0" />
                </path>
                <path stroke-dasharray="28" stroke-dashoffset="28" d="M2 10l10 -8l10 8">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="1.6s" dur="1.6s" values="28;0" />
                </path>
                <path stroke-dasharray="24" stroke-dashoffset="24" d="M9.5 21.5v-9h5v9">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="2.8s" dur="1.6s" values="24;0" />
                </path>
              </g>
            </svg>
            <span>Home</span>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'students'" class="menu-item flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <g fill="none" stroke="currentColor" stroke-dasharray="20" stroke-dashoffset="20" stroke-linecap="round" stroke-linejoin="round" stroke-width="2.8">
              <path d="M6 19v-1c0 -2.21 1.79 -4 4 -4h4c2.21 0 4 1.79 4 4v1">
                <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.8s" values="20;0" />
              </path>
              <path d="M12 11c-1.66 0 -3 -1.34 -3 -3c0 -1.66 1.34 -3 3 -3c1.66 0 3 1.34 3 3c0 1.66 -1.34 3 -3 3Z">
                <animate fill="freeze" attributeName="stroke-dashoffset" begin="0.8s" dur="0.8s" values="20;0" />
              </path>
            </g>
          </svg>
            <span>Students</span>
          </NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'applications'" class="menu-item flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
            <mask id="lineMdFileDocumentPlus0">
              <g fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2">
                <path stroke-dasharray="64" stroke-dashoffset="64" d="M13.5 3l5.5 5.5v11.5c0 0.55 -0.45 1 -1 1h-12c-0.55 0 -1 -0.45 -1 -1v-16c0 -0.55 0.45 -1 1 -1Z">
                  <animate fill="freeze" attributeName="stroke-dashoffset" dur="2.04s" values="64;0" />
                </path>
                <path d="M14.5 3.5l2.25 2.25l2.25 2.25z" opacity="0">
                  <animate fill="freeze" attributeName="d" begin="2.04s" dur="0.68s" values="M14.5 3.5l2.25 2.25l2.25 2.25z;M14.5 3.5l0 4.5l4.5 0z" />
                  <set fill="freeze" attributeName="opacity" begin="2.04s" to="1" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M9 13h6">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="2.72s" dur="0.68s" values="8;0" />
                </path>
                <path stroke-dasharray="4" stroke-dashoffset="4" d="M9 17h3">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="3.4s" dur="0.68s" values="4;0" />
                </path>
                <path fill="#000" fill-opacity="0" stroke="none" d="M19 13c3.31 0 6 2.69 6 6c0 3.31 -2.69 6 -6 6c-3.31 0 -6 -2.69 -6 -6c0 -3.31 2.69 -6 6 -6Z">
                  <set fill="freeze" attributeName="fill-opacity" begin="4.08s" to="1" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M16 19h6">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="4.08s" dur="0.68s" values="8;0" />
                </path>
                <path stroke-dasharray="8" stroke-dashoffset="8" d="M19 16v6">
                  <animate fill="freeze" attributeName="stroke-dashoffset" begin="4.76s" dur="0.68s" values="8;0" />
                </path>
              </g>
            </mask>
            <rect width="24" height="24" fill="currentColor" mask="url(#lineMdFileDocumentPlus0)" />
          </svg>
            <span>Applications</span>
          </NavigationMenuLink>
        </NavigationMenuItem>
      <NavigationMenuItem>
          <NavigationMenuLink
            @click="activeTab = 'schedule'"
            class="menu-item relative flex justify-center"
            style="width: 80px; height: 80px"
          >
            <!-- ICON -->
            <dotlottie-player
              class="absolute"
              src="https://lottie.host/2da353fe-c174-4f63-8789-da9359318733/CAV8nAVlPc.lottie"
              background="transparent"
              speed="1"
              mode="normal"                    
              autoplay 
              style="
                top: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 60px;
                height: 60px;
              "
            ></dotlottie-player>

            <!-- TEXT -->
            <span
              class="absolute text-sm"
              style="top: 45px; left: 50%; transform: translateX(-50%)"
            >
              Schedule
            </span>
          </NavigationMenuLink>
        </NavigationMenuItem>


      <NavigationMenuItem>
        <NavigationMenuLink
          @click="activeTab = 'analytics'"
          class="menu-item relative flex justify-center"
          style="width: 80px; height: 80px;"
        >
          <!-- ─── ICON (adjust top / left here) ─── -->
          <dotlottie-player
            class="absolute"
            src="https://lottie.host/2726b073-0576-480f-8c13-f9e069a1788c/RsBWOtzn9o.lottie"
            background="transparent"
            speed="1"
            mode="normal"                    
            autoplay                        
            style="
              top: 1px;                      /* raise or lower the icon */
              left: 50%;                     /* center horizontally */
              transform: translateX(-50%);
              width: 100px;
              height: 60px;
            "
          ></dotlottie-player>

          <!-- ─── TEXT (adjust top for the gap) ─── -->
          <span
            class="absolute text-sm"
            style="
              top: 45px;                     /* distance below the icon */
              left: 50%;
              transform: translateX(-50%);
            "
          >
            Analytics
          </span>
        </NavigationMenuLink>
</NavigationMenuItem>
        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'settings'" class="menu-item flex items-center space-x-2">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
              <mask id="lineMdCogFilledLoop0">
                <defs>
                  <symbol id="lineMdCogFilledLoop1">
                    <path d="M11 13L15.74 5.5C16.03 5.67 16.31 5.85 16.57 6.05C16.57 6.05 16.57 6.05 16.57 6.05C16.64 6.1 16.71 6.16 16.77 6.22C18.14 7.34 19.09 8.94 19.4 10.75C19.41 10.84 19.42 10.92 19.43 11C19.43 11 19.43 11 19.43 11C19.48 11.33 19.5 11.66 19.5 12z">
                      <animate fill="freeze" attributeName="d" begin="0.5s" dur="0.2s" values="M11 13L15.74 5.5C16.03 5.67 16.31 5.85 16.57 6.05C16.57 6.05 16.57 6.05 16.57 6.05C16.64 6.1 16.71 6.16 16.77 6.22C18.14 7.34 19.09 8.94 19.4 10.75C19.41 10.84 19.42 10.92 19.43 11C19.43 11 19.43 11 19.43 11C19.48 11.33 19.5 11.66 19.5 12z;M11 13L15.74 5.5C16.03 5.67 16.31 5.85 16.57 6.05C16.57 6.05 19.09 5.04 19.09 5.04C19.25 4.98 19.52 5.01 19.6 5.17C19.6 5.17 21.67 8.75 21.67 8.75C21.77 8.92 21.73 9.2 21.6 9.32C21.6 9.32 19.43 11 19.43 11C19.48 11.33 19.5 11.66 19.5 12z" />
                    </path>
                  </symbol>
                </defs>
                <g fill="none" stroke="#fff" stroke-width="2">
                  <path stroke-dasharray="36" stroke-dashoffset="36" stroke-width="5" d="M12 7c2.76 0 5 2.24 5 5c0 2.76 -2.24 5 -5 5c-2.76 0 -5 -2.24 -5 -5c0 -2.76 2.24 -5 5 -5Z">
                    <animate fill="freeze" attributeName="stroke-dashoffset" dur="0.5s" values="36;0" />
                    <set fill="freeze" attributeName="opacity" begin="0.5s" to="0" />
                  </path>
                  <g fill="#fff" stroke="none" opacity="0">
                    <use href="#lineMdCogFilledLoop1" />
                    <use href="#lineMdCogFilledLoop1" transform="rotate(60 12 12)" />
                    <use href="#lineMdCogFilledLoop1" transform="rotate(120 12 12)" />
                    <use href="#lineMdCogFilledLoop1" transform="rotate(180 12 12)" />
                    <use href="#lineMdCogFilledLoop1" transform="rotate(240 12 12)" />
                    <use href="#lineMdCogFilledLoop1" transform="rotate(300 12 12)" />
                    <set fill="freeze" attributeName="opacity" begin="0.5s" to="1" />
                    <animateTransform attributeName="transform" dur="30s" repeatCount="indefinite" type="rotate" values="0 12 12;360 12 12" />
                  </g>
                </g>
                <circle cx="12" cy="12" r="3.5" />
              </mask>
              <rect width="24" height="24" fill="currentColor" mask="url(#lineMdCogFilledLoop0)" />
            </svg>
            <span>Settings</span>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
      <NavigationMenuViewport class="mt-2 animate-slide-down" />
    </NavigationMenu>
  </div>

  <!-- Content Area -->
  <div class="relative z-10 flex justify-center items-start min-h-screen py-12 px-4">
    <div class="w-full max-w-6xl rounded-3xl bg-white/10 backdrop-blur-2xl shadow-2xl border border-[#3b82f6]/20 p-10 animate-fade-in glass-panel">
      <!-- Rare: SVG Title with animated gradient -->
      <svg class="w-full h-16 mb-8" viewBox="0 0 700 80">
        <defs>
          <linearGradient id="titleGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#6366f1" />
            <stop offset="33%" stop-color="#a21caf" />
            <stop offset="66%" stop-color="#3b82f6" />
            <stop offset="100%" stop-color="#6366f1" />
            <animate attributeName="x1" values="0;1;0" dur="12s" repeatCount="indefinite" />
            <animate attributeName="x2" values="1;0;1" dur="12s" repeatCount="indefinite" />
          </linearGradient>
        </defs>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="48" font-weight="bold" fill="url(#titleGradient)">
          Admission Dashboard
        </text>
      </svg>
      <HomeSection         v-if="activeTab === 'home'" />
      <StudentsSection     v-if="activeTab === 'students'" />
      <ApplicationsSection v-if="activeTab === 'applications'" />
      <ScheduleSection     v-if="activeTab === 'schedule'" />
      <AnalyticsSection    v-if="activeTab === 'analytics'" />
      <SettingsSection     v-if="activeTab === 'settings'" />
    </div>
  </div>
</template>

<style scoped>
.menu-item {
  @apply flex items-center space-x-2 transition-all duration-300 hover:text-yellow-300 hover:scale-105;
}
.glass-panel {
  box-shadow: 0 8px 40px 0 rgba(74, 222, 255, 0.14), 0 1.5px 8px 0 rgba(139, 92, 246, 0.11);
  border-radius: 2rem;
  border: 1.5px solid rgba(59, 130, 246, 0.18);
  background: linear-gradient(135deg, rgba(31,41,55,0.75) 0%, rgba(59,130,246,0.18) 100%);
  backdrop-filter: blur(32px) saturate(140%);
}
#dynamic-grid-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: 60px;
  grid-auto-rows: 60px;
  opacity: 0.15;
}
.grid-cell {
  background: transparent;
  border: 1px solid rgba(99, 102, 241, 0.05);
  transition: all 0.8s ease;
}
.grid-cell:hover {
  background: rgba(162, 28, 175, 0.1);
  border: 1px solid rgba(162, 28, 175, 0.2);
}
@keyframes fade-in {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes slide-down {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.6s ease forwards;
}
.animate-slide-down {
  animation: slide-down 0.3s ease forwards;
}
</style>
