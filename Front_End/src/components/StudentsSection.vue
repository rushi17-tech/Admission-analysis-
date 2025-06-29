<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

/*--------------------------------------------------------------------
  PROPS
-------------------------------------------------------------------*/
const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'students')

/*--------------------------------------------------------------------
  TYPES  – aligned with /students/accepted & /applications
-------------------------------------------------------------------*/
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

/*--------------------------------------------------------------------
  STATE
-------------------------------------------------------------------*/
const BASE_URL = 'http://localhost:8000/api'

const allEnrolled = ref<Student[]>([])
const allPending  = ref<Student[]>([])

const searchText     = ref('')
const selectedCourse = ref('')

const showEnrolled = ref(false)
const showPending  = ref(false)

/*--------------------------------------------------------------------
  FILTER HELPERS
-------------------------------------------------------------------*/
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

const enrolledStudents = computed(() =>
  allEnrolled.value.filter(passFilters)
)
const pendingStudents = computed(() =>
  allPending.value.filter(passFilters)
)

/*--------------------------------------------------------------------
  DATA FETCH
-------------------------------------------------------------------*/
onMounted(async () => {
  /* -------- accepted students -------- */
  try {
    const { data } = await axios.get<Student[]>(`${BASE_URL}/students/accepted`)
    allEnrolled.value = data
  } catch (err) {
    console.error('Failed /students/accepted → using fallback demo data', err)
    allEnrolled.value = [
      {
        id: 1,
        name: 'Demo Student',
        city: 'Vadodara',
        state: 'Gujarat',
        gender: 'female',
        score: 95,
        course: 'BCA',
        school: 'Sample School'
      }
    ]
  }

  /* -------- pending applications -------- */
  try {
    const { data } = await axios.get<ApplicationAPI[]>(`${BASE_URL}/applications`)
    allPending.value = data
      .filter((a) => a.status === 'pending')
      .map<Student>((a) => ({
        id:        a.application_id,
        name:      a.student_name,
        course:    a.course_name,
        /* placeholders (endpoint doesn’t return these) */
        city:      '',
        state:     '',
        gender:    '',
        score:     0,
        school:    ''
      }))
  } catch (err) {
    console.error('Failed /applications → using fallback demo data', err)
    allPending.value = [
      {
        id: 99,
        name: 'Pending Patel',
        city: '',
        state: '',
        gender: '',
        score: 0,
        course: 'MBA',
        school: ''
      }
    ]
  }
})

/*--------------------------------------------------------------------
  ACTIONS
-------------------------------------------------------------------*/
async function verifyStudent (s: Student) {
  try {
    await axios.patch(`${BASE_URL}/applications/${s.id}`, { status: 'accepted' })
  } catch (err) {
    console.warn('PATCH failed (optimistic update applied)', err)
  }
  /* move student from pending → enrolled */
  allPending.value  = allPending.value.filter((p) => p.id !== s.id)
  allEnrolled.value.push({ ...s, score: 0 }) // score unknown until entered
}
</script>

<template>
  <div
    v-if="activeTab === 'students'"
    class="py-8 px-2 md:px-8 bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 min-h-[80vh]"
  >
    <!-- ───── TITLE ───── -->
    <h3
      class="section-title text-3xl font-extrabold text-white mb-10 tracking-wide flex items-center gap-3"
    >
      <span
        class="inline-block bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent animate-pulse"
      >
        <svg
          class="w-8 h-8 inline-block mr-2"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path
            d="M12 14l9-5-9-5-9 5 9 5zm0 7v-6m0 0l-9-5m9 5l9-5"
          />
        </svg>
        Students Management
      </span>
    </h3>

    <!-- ───── SUMMARY CARDS ───── -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
      <!-- ENROLLED -->
      <div
        class="relative group bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-blue-500/30"
      >
        <span class="absolute top-4 right-4 text-blue-400 drop-shadow-lg">
          <svg
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87M16 3.13a4 4 0 0 1 0 7.75M8 3.13a4 4 0 1 0 0 7.75"
            />
          </svg>
        </span>
        <h4 class="text-xl font-bold text-white/90 mb-2">Total Enrolled</h4>
        <span
          class="text-5xl font-extrabold text-blue-400 drop-shadow-lg mb-4 animate-pulse"
        >
          {{ enrolledStudents.length }}
        </span>
        <button
          @click="showEnrolled = !showEnrolled"
          class="mt-2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg hover:from-blue-700 hover:to-purple-700 transition-all"
        >
          {{ showEnrolled ? 'Hide' : 'View' }} Enrolled
        </button>
      </div>

      <!-- PENDING -->
      <div
        class="relative group bg-white/10 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 p-8 flex flex-col items-center justify-center transition-all duration-300 hover:scale-105 hover:shadow-yellow-400/30"
      >
        <span class="absolute top-4 right-4 text-yellow-400 drop-shadow-lg">
          <svg
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path d="M12 8v4l3 3" />
            <circle cx="12" cy="12" r="10" />
          </svg>
        </span>
        <h4 class="text-xl font-bold text-white/90 mb-2">Pending Verification</h4>
        <span
          class="text-5xl font-extrabold text-yellow-400 drop-shadow-lg mb-4 animate-pulse"
        >
          {{ pendingStudents.length }}
        </span>
        <button
          @click="showPending = !showPending"
          class="mt-2 px-6 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-white rounded-full shadow-lg hover:from-yellow-600 hover:to-orange-600 transition-all"
        >
          {{ showPending ? 'Hide' : 'View' }} Pending
        </button>
      </div>
    </div>

    <!-- ───── ENROLLED MODAL ───── -->
    <transition name="fade">
      <div
        v-if="showEnrolled"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      >
        <div
          class="relative bg-white/90 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[80vh] p-8 flex flex-col border border-blue-200/50"
        >
          <button
            @click="showEnrolled = false"
            class="absolute top-4 right-4 text-gray-700 hover:text-red-600 text-3xl font-bold"
          >
            &times;
          </button>

          <h2
            class="text-2xl font-bold mb-6 text-blue-900 flex items-center gap-2"
          >
            <svg
              class="w-6 h-6 text-blue-400"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                d="M17 20h5v-2a4 4 0 0 0-3-3.87M9 20H4v-2a4 4 0 0 1 3-3.87"
              />
            </svg>
            Enrolled Students
          </h2>

          <div
            class="flex-1 overflow-y-auto rounded-xl border border-blue-100/50 bg-white/70"
          >
            <table class="w-full text-sm text-gray-900">
              <thead class="bg-blue-50 sticky top-0 text-blue-900 text-left">
                <tr>
                  <th class="p-3 border-b">#</th>
                  <th class="p-3 border-b">Name</th>
                  <th class="p-3 border-b">Course</th>
                  <th class="p-3 border-b">School</th>
                  <th class="p-3 border-b">City</th>
                  <th class="p-3 border-b">State</th>
                  <th class="p-3 border-b text-center">Score</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(student, index) in enrolledStudents"
                  :key="student.id"
                  class="hover:bg-blue-100/70 transition"
                >
                  <td class="p-3 text-center">{{ index + 1 }}</td>
                  <td class="p-3 font-medium text-gray-800">
                    {{ student.name }}
                  </td>
                  <td class="p-3">{{ student.course }}</td>
                  <td class="p-3">{{ student.school }}</td>
                  <td class="p-3">{{ student.city }}</td>
                  <td class="p-3">{{ student.state }}</td>
                  <td class="p-3 text-center text-blue-600 font-semibold">
                    {{ student.score }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </transition>

    <!-- ───── PENDING MODAL ───── -->
    <transition name="fade">
      <div
        v-if="showPending"
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm"
      >
        <div
          class="relative bg-white/90 rounded-2xl shadow-2xl w-[90vw] max-w-4xl h-[80vh] p-8 flex flex-col border border-yellow-200/50"
        >
          <button
            @click="showPending = false"
            class="absolute top-4 right-4 text-gray-700 hover:text-red-600 text-3xl font-bold"
          >
            &times;
          </button>

          <h2
            class="text-2xl font-bold mb-6 text-yellow-700 flex items-center gap-2"
          >
            <svg
              class="w-6 h-6 text-yellow-400"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path d="M12 8v4l3 3" />
              <circle cx="12" cy="12" r="10" />
            </svg>
            Pending Verification
          </h2>

          <div
            class="flex-1 overflow-y-auto rounded-xl border border-yellow-100/50 bg-white/70"
          >
            <table class="w-full text-sm text-gray-900">
              <thead class="bg-blue-50 sticky top-0 text-blue-900 text-left">
                <tr>
                  <th class="p-3 border-b">#</th>
                  <th class="p-3 border-b">Name</th>
                  <th class="p-3 border-b">Course</th>
                  <th class="p-3 border-b">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(student, index) in pendingStudents"
                  :key="student.id"
                  class="hover:bg-yellow-100/70 transition"
                >
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
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
