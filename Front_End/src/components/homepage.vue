<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
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

<!-- Content Area -->
<div class="p-10 h-[calc(100vh-80px)] bg-gray-100 animate-fade-in">
  <h2 class="text-2xl font-bold mb-6 text-gray-800">Admission Dashboard</h2>

  <!-- HOME Section -->
  <div v-if="activeTab === 'home'">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">Total Applications</h3>
        <p class="text-4xl font-bold text-blue-600">{{ applications.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">Enrolled Students</h3>
        <p class="text-4xl font-bold text-green-600">{{ enrolledStudents.length }}</p>
      </div>
      <div class="bg-white rounded-xl shadow-md p-6">
        <h3 class="text-xl font-semibold mb-4">Pending Verification</h3>
        <p class="text-4xl font-bold text-yellow-600">{{ pendingStudents.length }}</p>
      </div>
    </div>
  </div>

  <!-- STUDENTS Section -->
  <div v-if="activeTab === 'students'" class="space-y-8">
    <h3 class="section-title text-2xl font-bold text-gray-800">Students Management</h3>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="group">
        <div class="w-[300px] h-[300px] md:w-[350px] md:h-[350px] flex flex-col items-center justify-center bg-white rounded-2xl shadow-md p-4 ml-4">
          <h4 class="text-xl font-semibold text-gray-800">Total Enrolled</h4>
          <span class="text-4xl font-bold mt-2 text-blue-600">{{ enrolledStudents.length }}</span>
          <button @click="showEnrolled = !showEnrolled" class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
            {{ showEnrolled ? 'Hide' : 'View' }} Enrolled Students
          </button>
        </div>
      </div>
      <div class="group">
        <div class="w-[300px] h-[300px] md:w-[350px] md:h-[350px] flex flex-col items-center justify-center bg-white rounded-2xl shadow-md p-4 ml-auto">
          <h4 class="text-xl font-semibold text-gray-800">Pending Verification</h4>
          <span class="text-4xl font-bold mt-2 text-yellow-600">{{ pendingStudents.length }}</span>
          <button @click="showPending = !showPending" class="mt-4 px-4 py-2 bg-yellow-500 text-white rounded hover:bg-yellow-600">
            {{ showPending ? 'Hide' : 'View' }} Pending Students
          </button>
        </div>
      </div>
    </div>
    <div v-if="showEnrolled" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div class="relative bg-white rounded-xl shadow-lg w-[90vw] h-[80vh] p-8 flex flex-col">
        <button @click="showEnrolled = false" class="absolute top-4 right-4 text-gray-700 hover:text-red-600 text-2xl font-bold" aria-label="Close">&times;</button>
        <h2 class="text-lg font-bold mb-4 text-gray-800">Enrolled Students</h2>
        <div class="flex-1 overflow-y-auto">
          <table class="w-full border text-sm text-gray-900">
            <thead class="bg-gray-100 sticky top-0 text-gray-900">
              <tr>
                <th class="p-2 border">#</th>
                <th class="p-2 border">Name</th>
                <th class="p-2 border">Course</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in enrolledStudents" :key="student.id">
                <td class="p-2 border text-center">{{ index + 1 }}</td>
                <td class="p-2 border">{{ student.name }}</td>
                <td class="p-2 border">{{ student.course }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    <div v-if="showPending" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div class="relative bg-white rounded-xl shadow-lg w-[90vw] h-[80vh] p-8 flex flex-col">
        <button @click="showPending = false" class="absolute top-4 right-4 text-gray-7 hover:text-red-600 text-2xl font-bold" aria-label="Close">&times;</button>
        <h2 class="text-lg font-bold mb-4 text-gray-800">Pending Verification</h2>
        <div class="flex-1 overflow-y-auto">
          <table class="w-full border text-sm text-gray-900">
            <thead class="bg-gray-100 sticky top-0 text-gray-900">
              <tr>
                <th class="p-2 border">#</th>
                <th class="p-2 border">Name</th>
                <th class="p-2 border">Course</th>
                <th class="p-2 border">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(student, index) in pendingStudents" :key="student.id">
                <td class="p-2 border text-center">{{ index + 1 }}</td>
                <td class="p-2 border">{{ student.name }}</td>
                <td class="p-2 border">{{ student.course }}</td>
                <td class="p-2 border text-center">
                  <button @click="verifyStudent(student)" class="bg-green-500 px-3 py-1 text-white rounded hover:bg-green-600">
                    Verify
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <!-- APPLICATIONS Section -->
  <div v-if="activeTab === 'applications'">
    <h3 class="text-2xl font-bold mb-6 text-gray-800">Applications Overview</h3>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="group">
        <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
          <template #default>
            <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
              <h4 class="text-xl font-semibold text-gray-800">New Applications</h4>
              <span class="text-4xl font-bold mt-2 text-blue-600">{{ applications.length }}</span>
            </div>
          </template>
          <template #back>
            <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
              <h4 class="text-xl font-semibold">Details</h4>
              <p class="mt-2 text-sm text-gray-200 text-center">
                A total of {{ applications.length }} applications have been received.
                This indicates steady interest in our academic programs.
              </p>
            </div>
          </template>
        </FlipCard>
      </div>
      <div class="group">
        <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
          <template #default>
            <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
              <h4 class="text-xl font-semibold text-gray-800">Documents Pending</h4>
              <span class="text-4xl font-bold mt-2 text-yellow-600">21</span>
            </div>
          </template>
          <template #back>
            <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
              <h4 class="text-xl font-semibold">Details</h4>
              <p class="mt-2 text-sm text-gray-200 text-center">
                21 applications require additional documentation.
                Follow up with applicants to complete their submissions.
              </p>
            </div>
          </template>
        </FlipCard>
      </div>
      <div class="group">
        <FlipCard class="mx-auto w-[300px] h-[300px] md:w-[350px] md:h-[350px]">
          <template #default>
            <div class="flex flex-col items-center justify-center h-full bg-white rounded-2xl shadow-md p-4">
              <h4 class="text-xl font-semibold text-gray-800">Rejected Applications</h4>
              <span class="text-4xl font-bold mt-2 text-red-600">8</span>
            </div>
          </template>
          <template #back>
            <div class="flex flex-col items-center justify-center h-full bg-black text-white rounded-2xl p-4">
              <h4 class="text-xl font-semibold">Details</h4>
              <p class="mt-2 text-sm text-gray-200 text-center">
                8 applications were rejected due to eligibility criteria.
                Review rejection reasons for process improvements.
              </p>
            </div>
          </template>
        </FlipCard>
      </div>
    </div>
  </div>

  <!-- SCHEDULE Section -->
  <div v-if="activeTab === 'schedule'">
    <h3 class="text-2xl font-bold mb-6 text-gray-800">Entrance Exam Schedule</h3>
    <div class="bg-white rounded-xl shadow-md p-6">
      <div v-for="(event, index) in schedule" :key="index" class="mb-4 p-4 border-b">
        <h4 class="text-lg font-semibold">{{ event.title }}</h4>
        <div class="mt-2" v-html="event.description"></div>
      </div>
    </div>
  </div>

  <!-- ANALYTICS Section -->
  <div v-if="activeTab === 'analytics'">
    <h3 class="text-2xl font-bold mb-6 text-gray-800">Admission Analytics</h3>
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
