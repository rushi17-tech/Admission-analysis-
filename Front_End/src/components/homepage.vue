<script setup lang="ts">
import { ref, watch, onMounted, defineComponent } from 'vue'
import axios from 'axios'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuViewport
} from '@/components/ui/navigation-menu'
import { BarChart, Users, FilePlus2, CalendarDays } from 'lucide-vue-next'
import FlipCard from '@/components/flipcard.vue'
import AdmissionCharts from '@/components/AdmissionChart.vue'
import { useRouter } from 'vue-router'
import { VueFlip } from 'vue-flip'

interface Student {
  id: number
  name: string
  course: string
}

interface Application {
  application_id: number
  student_name: string
  course_name: string
  status: string
}

interface AnalyticsItem {
  id: number
  student_name: string
  course_name: string
  status: string
  score?: number
}

interface ScheduleItem {
  title: string
  description: string
}

const activeTab = ref('home')
const showEnrolled = ref(false)
const showPending = ref(false)
const analytics = ref<AnalyticsItem[]>([])
const applications = ref<Application[]>([])
const schedule = ref<ScheduleItem[]>([])
const enrolledStudents = ref<Student[]>([])
const pendingStudents = ref<Student[]>([])
const router = useRouter()
const BASE_URL = 'http://localhost:8000/api'

// Fetch data when tab changes
watch(activeTab, async (tab) => {
  try {
    if (tab === 'students') {
      await fetchStudentsData()
    } else if (tab === 'applications') {
      const res = await axios.get<Application[]>(`${BASE_URL}/applications`)
      applications.value = res.data
    } else if (tab === 'schedule') {
      const res = await axios.get<ScheduleItem[]>(`${BASE_URL}/schedule`)
      schedule.value = res.data
    } else if (tab === 'analytics') {
      const res = await axios.get<AnalyticsItem[]>(`${BASE_URL}/analytics`)
      analytics.value = res.data
    }
  } catch (err) {
    console.error('API fetch error:', err)
  }
})

// Fetch student data
async function fetchStudentsData() {
  try {
    // Fetch enrolled students
    const enrolledRes = await axios.get<{ id: number; name: string; course: string }[]>(`${BASE_URL}/students/accepted`)
    enrolledStudents.value = enrolledRes.data.map(s => ({
      id: s.id,
      name: s.name,
      course: s.course
    }))

    // Fetch pending applications
    const appsRes = await axios.get<Application[]>(`${BASE_URL}/applications`)
    const pendingApps = appsRes.data.filter(app => app.status === 'Pending')
    pendingStudents.value = pendingApps.map(app => ({
      id: app.application_id,
      name: app.student_name,
      course: app.course_name
    }))
  } catch (err) {
    console.error('Error fetching student data:', err)
  }
}

// Verify student (frontend + backend integration)
const verifyStudent = async (student: Student) => {
  try {
    await axios.patch(`${BASE_URL}/applications/${student.id}`, { 
      status: 'Accepted' 
    })
    enrolledStudents.value.push(student)
    pendingStudents.value = pendingStudents.value.filter(s => s.id !== student.id)
  } catch (err) {
    console.error('Verification failed:', err)
  }
}

// Initial data fetch
onMounted(async () => {
  if (activeTab.value === 'students') {
    await fetchStudentsData()
  }
})

const getCourseName = (desc: string): string => {
  // You can customize this if course name is added to description in future
  return 'Based on Application';
};

const getExamDate = (desc: string): string => {
  const match = desc.match(/<strong>(\d{1,2} [A-Za-z]+)<\/strong>/);
  return match ? match[1] : 'Unknown';
};

const getReportingTime = (desc: string): string => {
  const match = desc.match(/<strong>(\d{1,2}:\d{2} [APMapm]{2})<\/strong>/);
  return match ? match[1] : 'Unknown';
};

const extractRound = (title: string): string => {
  const match = title.match(/Round (\d+)/);
  return match ? match[1] : '?';
};

function logout() {

   localStorage.removeItem('token')
   router.push('/login')
}

const props = defineProps({
  activeTab: String,
  applications: {
    type: Array,
    default: () => []
  }
})




const flippedCard = ref(-1)
const showModal = ref(false)
const modalType = ref('')

function flipCard(idx) {
  flippedCard.value = idx
  if (idx === -1) {
    // Reset all flips
    setTimeout(() => { flippedCard.value = -1 }, 300)
  }
}
function openModal(type) {
  modalType.value = type
  showModal.value = true
}



</script>


<template>
<!-- Navigation -->
<div class="w-full bg-gradient-to-r from-[#1f2937] via-[#3b82f6] to-[#8b5cf6] p-4 shadow-xl animate-fade-in">
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
      <NavigationMenuItem>
        <NavigationMenuLink @click="activeTab = 'analytics'" class="menu-item flex items-center space-x-2">
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

   <div v-if="activeTab === 'home'">
    <section class="p-10 bg-gray-100">
      <h2 class="text-2xl font-bold mb-6 text-gray-800">Admission Analysis</h2>
      <AdmissionCharts />
    </section>
  </div>

   <!-- ────────── STUDENTS SECTION ────────── -->
<div v-if="activeTab === 'students'" class="py-8 px-2 md:px-8 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 min-h-[80vh]">
  <h3 class="section-title text-3xl font-extrabold text-white mb-10 tracking-wide flex items-center gap-3">
    <span class="inline-block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-pulse">
      <svg class="w-8 h-8 inline-block mr-2" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path d="M12 14l9-5-9-5-9 5 9 5zm0 7v-6m0 0l-9-5m9 5l9-5"/>
      </svg>
      Students Management
    </span>
  </h3>

  <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
    <!-- Total Enrolled -->
    <div class="relative group bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-blue-500/30">
      <span class="absolute top-4 right-4 text-blue-400 drop-shadow-lg">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87M16 3.13a4 4 0 0 1 0 7.75M8 3.13a4 4 0 1 0 0 7.75"/>
        </svg>
      </span>
      <h4 class="text-xl font-bold text-white/90 mb-2">Total Enrolled</h4>
      <span class="text-5xl font-extrabold text-blue-400 drop-shadow-lg mb-4 animate-pulse">
        {{ enrolledStudents.length }}
      </span>
      <button
        @click="showEnrolled = !showEnrolled"
        class="mt-2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg hover:from-blue-700 hover:to-purple-700 transition-all"
      >
        <span class="font-semibold tracking-wide">{{ showEnrolled ? 'Hide' : 'View' }} Enrolled</span>
      </button>
    </div>

    <!-- Pending Verification -->
    <div class="relative group bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-yellow-400/30">
      <span class="absolute top-4 right-4 text-yellow-400 drop-shadow-lg">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M12 8v4l3 3"/>
          <circle cx="12" cy="12" r="10"/>
        </svg>
      </span>
      <h4 class="text-xl font-bold text-white/90 mb-2">Pending Verification</h4>
      <span class="text-5xl font-extrabold text-yellow-400 drop-shadow-lg mb-4 animate-pulse">
        {{ pendingStudents.length }}
      </span>
      <button
        @click="showPending = !showPending"
        class="mt-2 px-6 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-full shadow-lg hover:from-yellow-600 hover:to-orange-600 transition-all"
      >
        <span class="font-semibold tracking-wide">{{ showPending ? 'Hide' : 'View' }} Pending</span>
      </button>
    </div>
    
  </div>

  <!-- Enrolled Modal -->
  <transition name="fade">
    <div
      v-if="showEnrolled"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
    >
      <div class="relative bg-white/90 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[80vh] p-8 flex flex-col border border-blue-200/50">
        <button
          @click="showEnrolled = false"
          class="absolute top-4 right-4 text-gray-700 hover:text-red-600 text-3xl font-bold"
          aria-label="Close"
        >&times;</button>
        <h2 class="text-2xl font-bold mb-6 text-blue-900 flex items-center gap-2">
          <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87"/>
          </svg>
          Enrolled Students
        </h2>
        <div class="flex-1 overflow-y-auto rounded-xl border border-blue-100/50 bg-white/70">
          <table class="w-full text-sm text-gray-900">
            <thead class="bg-blue-50 sticky top-0 text-blue-900">
              <tr>
                <th class="p-3 border-b">#</th>
                <th class="p-3 border-b">Name</th>
                <th class="p-3 border-b">Course</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in enrolledStudents" :key="student.id" class="hover:bg-blue-100/70 transition">
                <td class="p-3 text-center">{{ index + 1 }}</td>
                <td class="p-3">{{ student.name }}</td>
                <td class="p-3">{{ student.course }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </transition>

  <!-- Pending Modal -->
  <transition name="fade">
    <div
      v-if="showPending"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
    >
      <div class="relative bg-white/90 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[80vh] p-8 flex flex-col border border-yellow-200/50">
        <button
          @click="showPending = false"
          class="absolute top-4 right-4 text-gray-700 hover:text-red-600 text-3xl font-bold"
          aria-label="Close"
        >&times;</button>
        <h2 class="text-2xl font-bold mb-6 text-yellow-700 flex items-center gap-2">
          <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M12 8v4l3 3"/>
            <circle cx="12" cy="12" r="10"/>
          </svg>
          Pending Verification
        </h2>
        <div class="flex-1 overflow-y-auto rounded-xl border border-yellow-100/50 bg-white/70">
          <table class="w-full text-sm text-gray-900">
            <thead class="bg-yellow-50 sticky top-0 text-yellow-900">
              <tr>
                <th class="p-3 border-b">#</th>
                <th class="p-3 border-b">Name</th>
                <th class="p-3 border-b">Course</th>
                <th class="p-3 border-b">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in pendingStudents" :key="student.id" class="hover:bg-yellow-100/70 transition">
                <td class="p-3 text-center">{{ index + 1 }}</td>
                <td class="p-3">{{ student.name }}</td>
                <td class="p-3">{{ student.course }}</td>
                <td class="p-3 text-center">
                  <button
                    @click="verifyStudent(student)"
                    class="bg-gradient-to-r from-green-500 to-green-700 px-4 py-1 text-white rounded-full hover:from-green-600 hover:to-green-800 transition-all"
                  >
                    Verify
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </transition>
</div>

<!-- ────────── APPLICATIONS SECTION ────────── -->
     <div v-if="activeTab === 'applications'" class="p-6 futuristic-bg min-h-screen">
    <h3 class="text-4xl font-extrabold mb-10 text-white tracking-wide flex items-center gap-3 neon-text">
      <svg class="w-10 h-10 text-cyan-400 animate-pulse" fill="none" stroke="currentColor" stroke-width="2"
        viewBox="0 0 24 24"><path d="M12 4v16m8-8H4"></path></svg>
      Applications Overview
    </h3>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
      <!-- Card: New Applications -->
      <div class="relative perspective-1000 mx-auto" style="width:340px; height:400px;">
        <div
          class="flip-card"
          :class="{ flipped: flippedCard === 0 }"
        >
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-cyan-400 shadow-cyan-400/40">
            <svg class="w-12 h-12 text-cyan-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
              viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 00-3-3.87M6 21v-2a4 4 0 013-3.87m6-7a4 4 0 11-8 0 4 4 0 018 0zm6 4v6m3-3h-6"></path></svg>
            <h4 class="text-2xl font-bold neon-text mb-2">New Applications</h4>
            <span class="text-6xl font-extrabold mb-4 neon-text-cyan">{{ applications.length }}</span>
            <button
              class="mt-4 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(0)"
            >
              Show Details
            </button>
          </div>
          <!-- BACK -->
          <div class="flip-card-back glassmorphic-card border-cyan-400 shadow-cyan-400/40">
            <h4 class="text-xl font-semibold neon-text mb-2">Details</h4>
            <ul class="text-base text-white/90 text-center space-y-1 mb-4">
              <li>A total of <b>{{ applications.length }}</b> applications have been received.</li>
              <li>Interest in our programs remains high.</li>
              <li>All applications are currently under initial review.</li>
            </ul>
            <button
              class="mt-2 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(-1)"
            >
              Back
            </button>
          </div>
        </div>
      </div>

      <!-- Card: Documents Pending -->
      <div class="relative perspective-1000 mx-auto" style="width:340px; height:400px;">
        <div
          class="flip-card"
          :class="{ flipped: flippedCard === 1 }"
        >
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-amber-400 shadow-amber-400/40">
            <svg class="w-12 h-12 text-amber-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
              viewBox="0 0 24 24"><path d="M7 7h10M7 11h10M7 15h6M5 19h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
            <h4 class="text-2xl font-bold neon-text mb-2">Documents Pending</h4>
            <span class="text-6xl font-extrabold mb-4 neon-text-amber">21</span>
            <button
              class="mt-4 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(1)"
            >
              Show Details
            </button>
          </div>
          <!-- BACK -->
          <div class="flip-card-back glassmorphic-card border-amber-400 shadow-amber-400/40">
            <h4 class="text-xl font-semibold neon-text mb-2">Details</h4>
            <ul class="text-base text-white/90 text-center space-y-1 mb-4">
              <li>21 applications require additional documentation.</li>
              <li>Most common reasons:</li>
              <li>- <b>Missing transcripts</b> (12)</li>
              <li>- <b>Unverified ID proofs</b> (5)</li>
              <li>- <b>Incomplete application forms</b> (4)</li>
              <li>Applicants have been notified via email and SMS.</li>
            </ul>
            <button
              class="mb-2 px-5 py-1 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="openModal('pending')"
            >
              View More
            </button>
            <button
              class="mt-2 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(-1)"
            >
              Back
            </button>
          </div>
        </div>
      </div>

      <!-- Card: Rejected Applications -->
      <div class="relative perspective-1000 mx-auto" style="width:340px; height:400px;">
        <div
          class="flip-card"
          :class="{ flipped: flippedCard === 2 }"
        >
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-rose-400 shadow-rose-400/40">
            <svg class="w-12 h-12 text-rose-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
              viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4" y1="4" x2="20" y2="20"/></svg>
            <h4 class="text-2xl font-bold neon-text mb-2">Rejected Applications</h4>
            <span class="text-6xl font-extrabold mb-4 neon-text-rose">8</span>
            <button
              class="mt-4 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(2)"
            >
              Show Details
            </button>
          </div>
          <!-- BACK -->
          <div class="flip-card-back glassmorphic-card border-rose-400 shadow-rose-400/40">
            <h4 class="text-xl font-semibold neon-text mb-2">Details</h4>
            <ul class="text-base text-white/90 text-center space-y-1 mb-4">
              <li>8 applications have been rejected.</li>
              <li>Top rejection reasons:</li>
              <li>- <b>Did not meet eligibility criteria</b> (5)</li>
              <li>- <b>Late submission</b> (2)</li>
              <li>- <b>Invalid documents</b> (1)</li>
              <li>Applicants have been notified with feedback.</li>
            </ul>
            <button
              class="mb-2 px-5 py-1 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="openModal('rejected')"
            >
              View More
            </button>
            <button
              class="mt-2 px-6 py-2 bg-gradient-to-r from-white/10 to-white/30 border border-white/20 rounded-full neon-border shadow hover:scale-105 transition"
              @click="flipCard(-1)"
            >
              Back
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL FOR MORE DETAILS -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur"
    >
      <div class="bg-gradient-to-br from-gray-900/90 to-gray-800/80 border-2 border-white/10 rounded-2xl p-8 shadow-2xl w-full max-w-md">
        <h4 class="text-2xl font-bold neon-text mb-4">Detailed Reasons</h4>
        <ul class="space-y-3">
          <template v-if="modalType === 'pending'">
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Missing Transcripts</span>
              <span class="text-sm text-white/70">Count: 12</span>
              <span class="text-xs text-cyan-200">Awaiting upload from applicant.</span>
            </li>
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Unverified ID Proofs</span>
              <span class="text-sm text-white/70">Count: 5</span>
              <span class="text-xs text-cyan-200">Verification in progress.</span>
            </li>
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Incomplete Forms</span>
              <span class="text-sm text-white/70">Count: 4</span>
              <span class="text-xs text-cyan-200">Applicants need to fill all required fields.</span>
            </li>
          </template>
          <template v-else>
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Eligibility Not Met</span>
              <span class="text-sm text-white/70">Count: 5</span>
              <span class="text-xs text-cyan-200">Did not meet minimum academic requirements.</span>
            </li>
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Late Submission</span>
              <span class="text-sm text-white/70">Count: 2</span>
              <span class="text-xs text-cyan-200">Applications received after deadline.</span>
            </li>
            <li class="flex flex-col bg-white/10 p-3 rounded-lg neon-border">
              <span class="font-semibold text-lg neon-text">Invalid Documents</span>
              <span class="text-sm text-white/70">Count: 1</span>
              <span class="text-xs text-cyan-200">Submitted documents could not be verified.</span>
            </li>
          </template>
        </ul>
        <button
          class="mt-6 px-6 py-2 bg-gradient-to-r from-cyan-400 to-cyan-700 text-white rounded-full shadow hover:scale-105 transition"
          @click="showModal = false"
        >
          Close
        </button>
      </div>
    </div>
  </div>
   
<!-- ────────── SCHEDULE SECTION ────────── -->
<div v-if="activeTab === 'schedule'" class="p-6 space-y-6">
  <h3 class="text-2xl font-bold text-gray-800 mb-4">Entrance Exam Schedule</h3>

  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

    <!-- BCA Entrance -->
    <div class="group">
      <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
        <template #default>
          <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
            <h4 class="text-xl font-semibold text-gray-800">BCA Entrance Test</h4>
            <span class="text-4xl font-bold mt-2 text-blue-600">120</span>
          </div>
        </template>
        <template #back>
          <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
            <h4 class="text-xl font-semibold">Details</h4>
            <p class="mt-2 text-sm text-gray-200 text-center">
              📚 Course: BCA<br />
              📅 Date: 5th July 2025<br />
              ⏰ Time: 9:00 AM<br />
              🏫 Room No: A101<br />
              🔁 Round: 1
            </p>
          </div>
        </template>
      </FlipCard>
    </div>

    <!-- BBA Entrance -->
    <div class="group">
      <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
        <template #default>
          <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
            <h4 class="text-xl font-semibold text-gray-800">BBA Entrance Test</h4>
            <span class="text-4xl font-bold mt-2 text-green-600">90</span>
          </div>
        </template>
        <template #back>
          <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
            <h4 class="text-xl font-semibold">Details</h4>
            <p class="mt-2 text-sm text-gray-200 text-center">
              📚 Course: BBA<br />
              📅 Date: 6th July 2025<br />
              ⏰ Time: 10:30 AM<br />
              🏫 Room No: B203<br />
              🔁 Round: 1
            </p>
          </div>
        </template>
      </FlipCard>
    </div>

    <!-- B.Tech Entrance -->
    <div class="group">
      <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
        <template #default>
          <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
            <h4 class="text-xl font-semibold text-gray-800">B.Tech Entrance Test</h4>
            <span class="text-4xl font-bold mt-2 text-red-600">150</span>
          </div>
        </template>
        <template #back>
          <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
            <h4 class="text-xl font-semibold">Details</h4>
            <p class="mt-2 text-sm text-gray-200 text-center">
              📚 Course: B.Tech<br />
              📅 Date: 7th July 2025<br />
              ⏰ Time: 11:00 AM<br />
              🏫 Room No: C307<br />
              🔁 Round: 1
            </p>
          </div>
        </template>
      </FlipCard>
    </div>

    <!-- MBA Entrance -->
    <div class="group">
      <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
        <template #default>
          <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
            <h4 class="text-xl font-semibold text-gray-800">MBA Entrance Test</h4>
            <span class="text-4xl font-bold mt-2 text-purple-600">70</span>
          </div>
        </template>
        <template #back>
          <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
            <h4 class="text-xl font-semibold">Details</h4>
            <p class="mt-2 text-sm text-gray-200 text-center">
              📚 Course: MBA<br />
              📅 Date: 8th July 2025<br />
              ⏰ Time: 1:00 PM<br />
              🏫 Room No: D102<br />
              🔁 Round: 2
            </p>
          </div>
        </template>
      </FlipCard>
    </div>

  </div>
</div>


    <!-- ────────── ANALYTICS SECTION ────────── -->
    <div v-if="activeTab === 'analytics'">
      <h3 class="text-2xl font-bold mb-6 text-gray-800">
        Admission Analytics
      </h3>
      <div class="bg-white rounded-xl shadow-md p-6 overflow-x-auto">
        <table class="w-full border text-sm text-gray-900">
          <thead class="bg-gray-100 text-gray-900">
            <tr>
              <th class="p-2 border">ID</th>
              <th class="p-2 border">Student</th>
              <th class="p-2 border">Course</th>
              <th class="p-2 border">Status</th>
              <th class="p-2 border">Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in analytics" :key="item.id">
              <td class="p-2 border text-center">{{ item.id }}</td>
              <td class="p-2 border">{{ item.student_name }}</td>
              <td class="p-2 border">{{ item.course_name }}</td>
              <td class="p-2 border">{{ item.status }}</td>
              <td class="p-2 border">{{ item.score || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ────────── SETTINGS SECTION ────────── -->
<!-- ────────── SETTINGS SECTION ────────── -->
<div v-if="activeTab === 'settings'" class="p-6 space-y-6">
  <h3 class="text-2xl font-bold mb-6 text-gray-800">Settings</h3>

  <div class="bg-white rounded-xl shadow-md p-6 max-w-sm">
    <!-- ⚙️  Settings Item -->
    <button
      @click="logout"
      class="w-full flex items-center justify-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition"
    >
      🔒 Logout
    </button>
  </div>
</div>


  </div>
</template>

<style scoped>

.futuristic-bg {
  background: linear-gradient(135deg, #0f2027 0%, #2c5364 100%);
  min-height: 100vh;
}
.glassmorphic-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(0,255,255,0.08));
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
  border-radius: 30px;
  border: 2px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(8px);
  width: 100%;
  height: 100%;
  padding: 2.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0; left: 0;
  backface-visibility: hidden;
  transition: box-shadow 0.3s;
}
.perspective-1000 {
  perspective: 1000px;
}
.flip-card {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.7s cubic-bezier(.4,2.3,.3,1);
}
.flip-card-front {
  z-index: 2;
}
.flip-card-back {
  transform: rotateY(180deg);
  z-index: 1;
}
.flip-card.flipped {
  transform: rotateY(180deg);
}
.neon-text {
  text-shadow: 0 0 8px #00fff7, 0 0 2px #fff;
}
.neon-text-cyan {
  color: #00fff7;
  text-shadow: 0 0 10px #00fff7, 0 0 2px #fff;
}
.neon-text-amber {
  color: #ffc107;
  text-shadow: 0 0 10px #ffc107, 0 0 2px #fff;
}
.neon-text-rose {
  color: #ff007a;
  text-shadow: 0 0 10px #ff007a, 0 0 2px #fff;
}
.neon-border {
  box-shadow: 0 0 8px #00fff7, 0 0 2px #fff;
}

.shadow-xl {
  box-shadow: 0 10px 25px rgba(30, 64, 175, 0.15), 0 2px 4px rgba(0,0,0,0.08);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
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
