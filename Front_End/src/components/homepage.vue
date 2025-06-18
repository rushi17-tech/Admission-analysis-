<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuViewport
} from '@/components/ui/navigation-menu'

import { BarChart, Users, FilePlus2, CalendarDays } from 'lucide-vue-next'

const activeTab = ref('home')

// Dynamic data containers
const analytics = ref({})
const students = ref({})
const applications = ref({})
const schedule = ref({})

// Watcher to fetch data on tab change
watch(activeTab, async (tab) => {
  try {
    const res = await axios.get(`http://localhost:8000/${tab}`)
    if (tab === 'analytics') analytics.value = res.data
    else if (tab === 'students') students.value = res.data
    else if (tab === 'applications') applications.value = res.data
    else if (tab === 'schedule') schedule.value = res.data
  } catch (err) {
    console.error('API fetch error:', err)
  }
})
</script>

<template>
  <!-- Navigation -->
  <div class="w-full bg-gradient-to-r from-[#1f2937] via-[#3b82f6] to-[#8b5cf6] p-4 shadow-xl animate-fade-in">
    <NavigationMenu>
      <NavigationMenuList>
        <!-- Home Tab with Animated SVG -->
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

        <!-- Other Tabs -->
        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'analytics'" class="menu-item flex items-center space-x-2">
            <BarChart class="w-5 h-5" />
            <span>Analytics</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'students'" class="menu-item flex items-center space-x-2">
            <Users class="w-5 h-5" />
            <span>Students</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'applications'" class="menu-item flex items-center space-x-2">
            <FilePlus2 class="w-5 h-5" />
            <span>Applications</span>
          </NavigationMenuLink>
        </NavigationMenuItem>

        <NavigationMenuItem>
          <NavigationMenuLink @click="activeTab = 'schedule'" class="menu-item flex items-center space-x-2">
            <CalendarDays class="w-5 h-5" />
            <span>Schedule</span>
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
      <NavigationMenuViewport class="mt-2 animate-slide-down" />
    </NavigationMenu>
  </div>

  <!-- Content Area -->
  <div class="p-10 h-[calc(100vh-80px)] bg-gray-100 animate-fade-in">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">University Admission Panel</h2>

    <div v-if="activeTab === 'home'">
      <p class="text-gray-700">Welcome to the university dashboard. Select a menu item to begin.</p>
    </div>

    <div v-if="activeTab === 'analytics'">
      <h3 class="section-title">Analytics</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="stat-card">Daily Applications<br /><span class="highlight">56</span></div>
        <div class="stat-card">Conversion Rate<br /><span class="highlight">38%</span></div>
        <div class="stat-card">Top Course Today<br /><span class="highlight">B.Tech CSE</span></div>
      </div>
    </div>

    <div v-if="activeTab === 'students'">
      <h3 class="section-title">Students Overview</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="stat-card">Total Enrolled<br /><span class="highlight">1450</span></div>
        <div class="stat-card">Pending Verification<br /><span class="highlight">72</span></div>
        <div class="stat-card">Dropouts<br /><span class="highlight">14</span></div>
      </div>
    </div>

    <div v-if="activeTab === 'applications'">
      <h3 class="section-title">Applications</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="stat-card">New Applications<br /><span class="highlight">103</span></div>
        <div class="stat-card">Documents Pending<br /><span class="highlight">21</span></div>
        <div class="stat-card">Reviewed Today<br /><span class="highlight">89</span></div>
      </div>
    </div>

    <div v-if="activeTab === 'schedule'">
      <h3 class="section-title">Upcoming Schedule</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="stat-card">Entrance Exam - B.Tech<br /><span class="highlight">22nd June</span></div>
        <div class="stat-card">Interview Round - MBA<br /><span class="highlight">25th June</span></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.menu-item {
  @apply flex items-center space-x-2 transition-all duration-300 hover:text-yellow-300 hover:scale-105 hover:drop-shadow-lg;
}
.stat-card {
  @apply bg-white p-6 rounded-xl shadow-xl text-center text-lg font-medium transition-all duration-300;
}
.stat-card:hover {
  background: linear-gradient(to right, #60a5fa, #c084fc);
  color: white;
  transform: scale(1.05);
}
.highlight {
  @apply text-indigo-700 text-2xl font-bold;
}
.section-title {
  @apply text-xl font-semibold text-gray-700 mb-4;
}
@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes slide-down {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in {
  animation: fade-in 0.6s ease forwards;
}
.animate-slide-down {
  animation: slide-down 0.3s ease forwards;
}
</style>
