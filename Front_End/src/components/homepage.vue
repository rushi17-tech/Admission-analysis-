<script setup lang="ts">
/* ────────── Core imports ────────── */
import { ref } from 'vue'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuViewport
} from '@/components/ui/navigation-menu'
import { BarChart, Users, FilePlus2, CalendarDays } from 'lucide-vue-next'

/* ────────── Split‑out tab components ────────── */
import HomeSection         from '@/components/HomeSection.vue'
import StudentsSection     from '@/components/StudentsSection.vue'
import ApplicationsSection from '@/components/ApplicationsSection.vue'
import ScheduleSection     from '@/components/ScheduleSection.vue'
import AnalyticsSection    from '@/components/AnalyticsSection.vue'
import SettingsSection     from '@/components/SettingsSection.vue'

/* ────────── UI state ────────── */
const activeTab = ref<
  'home' | 'students' | 'applications' | 'schedule' | 'analytics' | 'settings'
>('home')
</script>

<template>
  <!-- ────────── NAVIGATION BAR ────────── -->
  <div
    class="w-full bg-gradient-to-r from-[#1f2937] via-[#3b82f6] to-[#8b5cf6] p-4 shadow-xl animate-fade-in"
  >
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
          <NavigationMenuLink
            @click="activeTab = 'students'"
            class="menu-item flex items-center space-x-2"
          >
            <Users class="w-5 h-5" />
            <span>Students</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink
            @click="activeTab = 'applications'"
            class="menu-item flex items-center space-x-2"
          >
            <FilePlus2 class="w-5 h-5" />
            <span>Applications</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink
            @click="activeTab = 'schedule'"
            class="menu-item flex items-center space-x-2"
          >
            <CalendarDays class="w-5 h-5" />
            <span>Schedule</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink
            @click="activeTab = 'analytics'"
            class="menu-item flex items-center space-x-2"
          >
            <BarChart class="w-5 h-5" />
            <span>Analytics</span>
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

  <!-- ────────── CONTENT AREA ────────── -->
  <div class="p-10 bg-gray-100 min-h-screen overflow-y-auto animate-fade-in">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Admission Dashboard</h2>

    <HomeSection         v-if="activeTab === 'home'" />
    <StudentsSection     v-if="activeTab === 'students'" />
    <ApplicationsSection v-if="activeTab === 'applications'" />
    <ScheduleSection     v-if="activeTab === 'schedule'" />
    <AnalyticsSection    v-if="activeTab === 'analytics'" />
    <SettingsSection     v-if="activeTab === 'settings'" />
  </div>
</template>

<style scoped>
.menu-item {
  @apply flex items-center space-x-2 transition-all duration-300 hover:text-yellow-300
    hover:scale-105 hover:drop-shadow-lg;
}
@keyframes fade-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.6s ease forwards;
}
.animate-slide-down {
  animation: slide-down 0.3s ease forwards;
}
</style>
