<script setup lang="ts">
/* ───────────── imports / props / state (UNCHANGED) ───────────── */
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'students')

interface Student {
  id: number
  name: string
  city: string
  state: string
  gender: string
  score: number
  course: string
  school: string
}
interface ApplicationAPI {
  application_id: number
  student_name: string
  course_name: string
  status: 'pending' | 'accepted' | 'rejected'
}

const BASE_URL       = 'http://localhost:8000/api'
const allEnrolled    = ref<Student[]>([])
const allPending     = ref<Student[]>([])
const searchText     = ref('')
const selectedCourse = ref('')
const showEnrolled   = ref(false)
const showPending    = ref(false)

function passFilters (s: Student) {
  const q = searchText.value.toLowerCase()
  const okSearch =
    !q ||
    s.name.toLowerCase().includes(q) ||
    s.city.toLowerCase().includes(q) ||
    s.state.toLowerCase().includes(q)
  const okCourse = !selectedCourse.value || s.course === selectedCourse.value
  return okSearch && okCourse
}
const enrolledStudents = computed(() => allEnrolled.value.filter(passFilters))
const pendingStudents  = computed(() => allPending.value.filter(passFilters))

/* --------------------- fetch (UNCHANGED) ---------------------- */
onMounted(async () => {
  try {
    const { data } = await axios.get<Student[]>(`${BASE_URL}/students/accepted`)
    allEnrolled.value = data
  } catch (err) {
    console.error('Failed /students/accepted – fallback demo data', err)
    allEnrolled.value = [{
      id: 1, name: 'Demo Student', city: 'Vadodara', state: 'Gujarat',
      gender: 'female', score: 95, course: 'BCA', school: 'Sample School'
    }]
  }

  try {
    const { data } = await axios.get<ApplicationAPI[]>(`${BASE_URL}/applications`)
    allPending.value = data
      .filter(a => a.status === 'pending')
      .map<Student>(a => ({
        id: a.application_id, name: a.student_name, course: a.course_name,
        city: '', state: '', gender: '', score: 0, school: ''
      }))
  } catch (err) {
    console.error('Failed /applications – fallback demo data', err)
    allPending.value = [{
      id: 99, name: 'Pending Patel', city: '', state: '',
      gender: '', score: 0, course: 'MBA', school: ''
    }]
  }
})

async function verifyStudent (s: Student) {
  try { await axios.patch(`${BASE_URL}/applications/${s.id}`, { status: 'accepted' }) }
  catch (err) { console.warn('PATCH failed (optimistic update)', err) }

  allPending.value  = allPending.value.filter(p => p.id !== s.id)
  allEnrolled.value.push({ ...s, score: 0 })
}
</script>

<template>
  <div
    v-if="activeTab === 'students'"
    class="relative py-10 px-3 md:px-10 min-h-[82vh] animate-fade-in"
  >
    <!-- ───── title ───── -->
    <h3 class="section-title mb-10 text-4xl font-extrabold tracking-wide flex items-center gap-3">
      <span class="inline-flex items-center gap-3 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
        <svg class="w-9 h-9" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M12 14l9-5-9-5-9 5 9 5zm0 7v-6m0 0l-9-5m9 5l9-5"/>
        </svg>
        Students&nbsp;Management
      </span>
    </h3>

    <!-- ───── summary cards ───── -->
    <div class="grid gap-8 grid-cols-[repeat(auto-fit,minmax(250px,1fr))]">
      <!-- enrolled -->
      <div class="glass-card group hover:shadow-blue-500/40">
        <span class="card-icon text-blue-300">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87M16 3.13a4 4 0 0 1 0 7.75M8 3.13a4 4 0 1 0 0 7.75"/>
          </svg>
        </span>

        <h4 class="card-label">Total&nbsp;Enrolled</h4>
        <span class="card-count text-blue-300">{{ enrolledStudents.length }}</span>

        <button
          @click="showEnrolled = !showEnrolled"
          class="card-btn bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
        >
          {{ showEnrolled ? 'Hide' : 'View' }}&nbsp;Enrolled
        </button>
      </div>

      <!-- pending / accept -->
      <div class="glass-card group hover:shadow-yellow-400/40">
        <span class="card-icon text-yellow-300">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/>
          </svg>
        </span>

        <h4 class="card-label">Accept&nbsp;Students</h4>
        <span class="card-count text-yellow-300">{{ pendingStudents.length }}</span>

        <button
          @click="showPending = !showPending"
          class="card-btn bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600"
        >
          {{ showPending ? 'Hide' : 'View' }}&nbsp;To&nbsp;Accept
        </button>
      </div>
    </div>

    <!-- ───── enrolled modal ───── -->
    <transition name="fade">
      <div v-if="showEnrolled" class="modal-backdrop">
        <div class="modal-window border-blue-200/40">
          <button @click="showEnrolled = false" class="modal-close">&times;</button>

          <h2 class="modal-title text-blue-900">
            <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87"/>
            </svg>
            Enrolled Students
          </h2>

          <input v-model="searchText" type="text" placeholder="Search students…" class="modal-search focus:ring-blue-400"/>

          <div class="modal-table-wrapper border-blue-100/40">
            <table class="modal-table">
              <thead class="sticky top-0 bg-blue-50 text-blue-900">
                <tr>
                  <th>#</th><th>Name</th><th>Course</th><th>School</th><th>City</th><th>State</th><th class="text-center">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(student, i) in enrolledStudents" :key="student.id" class="hover:bg-blue-50/70">
                  <td class="text-center">{{ i + 1 }}</td>
                  <td class="font-medium">{{ student.name }}</td>
                  <td>{{ student.course }}</td>
                  <td>{{ student.school }}</td>
                  <td>{{ student.city }}</td>
                  <td>{{ student.state }}</td>
                  <td class="text-center text-blue-600 font-semibold">{{ student.score }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </transition>

    <!-- ───── pending modal ───── -->
    <transition name="fade">
      <div v-if="showPending" class="modal-backdrop">
        <div class="modal-window border-yellow-200/40">
          <button @click="showPending = false" class="modal-close">&times;</button>

          <h2 class="modal-title text-yellow-700">
            <svg class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M12 8v4l3 3"/><circle cx="12" cy="12" r="10"/>
            </svg>
            Accept Students
          </h2>

          <input v-model="searchText" type="text" placeholder="Search students…" class="modal-search focus:ring-yellow-400"/>

          <div class="modal-table-wrapper border-yellow-100/40">
            <table class="modal-table">
              <thead class="sticky top-0 bg-yellow-50 text-yellow-900">
                <tr><th>#</th><th>Name</th><th>Course</th><th class="text-center">Action</th></tr>
              </thead>
              <tbody>
                <tr v-for="(student, i) in pendingStudents" :key="student.id" class="hover:bg-yellow-50/70">
                  <td class="text-center">{{ i + 1 }}</td>
                  <td>{{ student.name }}</td>
                  <td>{{ student.course }}</td>
                  <td class="text-center">
                    <button @click="verifyStudent(student)" class="accept-btn">Accept</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* ───── reusable glass styles ───── */
.glass-card{
  @apply relative flex flex-col items-center justify-center p-9 rounded-3xl
          bg-white/5 backdrop-blur-2xl
          border border-white/15 shadow-xl
          transition-all duration-300 hover:scale-105;
}
.card-icon   { @apply absolute top-4 right-4 drop-shadow-lg; }
.card-label  { @apply text-xl font-bold text-white/90 mb-1; }
.card-count  { @apply text-5xl font-extrabold drop-shadow-lg mb-5 animate-pulse; }
.card-btn    { @apply mt-auto px-6 py-2 text-white rounded-full shadow-lg transition-all; }

/* ───── modal base ───── */
.modal-backdrop{ @apply fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-md; }
.modal-window  { @apply relative bg-white/90 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[80vh] p-8 flex flex-col overflow-hidden; }
.modal-close   { @apply absolute top-4 right-4 text-gray-700 hover:text-red-600 text-3xl font-bold; }
.modal-title   { @apply text-2xl font-bold mb-4 flex items-center gap-2; }
.modal-search  { @apply w-full mb-4 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2; }
.modal-table-wrapper{ @apply flex-1 overflow-y-auto rounded-xl bg-white/70 border; }
.modal-table   { @apply w-full text-sm text-gray-900; }

/* accept button inside pending modal */
.accept-btn{ @apply bg-gradient-to-r from-green-500 to-green-700 px-4 py-1 text-white rounded-full hover:from-green-600 hover:to-green-800 transition-all; }

/* ───── fade transition (unchanged) ───── */
.fade-enter-active, .fade-leave-active{ transition: opacity .3s; }
.fade-enter-from,   .fade-leave-to    { opacity: 0; }

/* ───── global entry animation ───── */
@keyframes fadeIn{ from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.animate-fade-in{ animation: fadeIn .6s ease forwards; }
</style>
