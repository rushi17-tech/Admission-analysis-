<template>
  <div class="space-y-6">
    <!-- ────────── FILTER BAR ────────── -->
    <div class="flex flex-wrap gap-4">
      <!-- Course filter -->
      <div class="relative">
        <button
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow"
          @click="courseDropdownOpen = !courseDropdownOpen"
        >
          {{ selectedCourse }} ▾
        </button>

        <div
          v-if="courseDropdownOpen"
          class="absolute z-10 mt-2 w-48 bg-white border rounded-lg shadow-lg"
        >
          <ul>
            <li
              v-for="course in courses"
              :key="course"
              @click="selectCourse(course)"
              class="px-4 py-2 hover:bg-indigo-100 cursor-pointer whitespace-nowrap text-gray-800"
            >
              {{ course }}
            </li>
          </ul>
        </div>
      </div>

      <!-- City multi-select -->
      <div class="relative">
        <button
          class="px-4 py-2 bg-emerald-600 text-white rounded-lg shadow"
          @click="dropdownOpen = !dropdownOpen"
        >
          Cities ({{ selectedCities.length }}) ▾
        </button>

        <div
          v-if="dropdownOpen"
          class="absolute z-10 mt-2 w-60 bg-white border rounded-lg shadow-lg p-4"
        >
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search city…"
            class="w-full mb-3 px-2 py-1 border rounded text-gray-800"
          />

          <label class="flex items-center mb-2 text-gray-800">
            <input type="checkbox" v-model="allSelected" class="mr-2" />
            Select all
          </label>

          <div class="h-40 overflow-y-auto pr-2">
            <label
              v-for="city in filteredCities"
              :key="city"
              class="flex items-center mb-1 cursor-pointer text-gray-800"
            >
              <input
                type="checkbox"
                :value="city"
                v-model="selectedCities"
                class="mr-2"
              />
              {{ city }}
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- ────────── CHART GRID ────────── -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="h-[400px]">
        <Bar :data="filteredCityData" :options="barOptions" />
      </div>
      <div class="h-[400px]">
        <Bar :data="scoreBarData" :options="scoreOptions" />
      </div>
      <div class="h-[400px]">
        <Pie :data="pieData" />
      </div>
      <div class="h-[400px]">
        <Pie :data="statusPieData" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/* ───────────── Imports ───────────── */
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  BarElement, ArcElement
} from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'
import { ref, computed, watch } from 'vue'

ChartJS.register(
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  BarElement, ArcElement
)

/* ───────────── STATIC DATA (90 students) ───────────── */
type Row = {
  id: number
  course: string
  city: string
  gender: 'Male' | 'Female'
  status: 'Accepted' | 'Pending' | 'Rejected'
  score: number
}

const CITIES = [
  'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar',
  'Bharuch', 'Jamnagar', 'Bhavnagar', 'Junagadh', 'Navsari'
]

function makeRows (startId: number, course: string): Row[] {
  const rows: Row[] = []
  let id = startId
  CITIES.forEach((city, i) => {
    // Three students per city: Accepted, Pending, Rejected
    rows.push(
      { id: id++, course, city, gender: i % 2 ? 'Female' : 'Male',   status: 'Accepted', score: 78 + (i % 5) },
      { id: id++, course, city, gender: i % 2 ? 'Male'   : 'Female', status: 'Pending',  score: 65 + (i % 7) },
      { id: id++, course, city, gender: i % 2 ? 'Female' : 'Male',   status: 'Rejected', score: 55 + (i % 6) }
    )
  })
  return rows
}

const applications = ref<Row[]>([
  ...makeRows(1,  'BCA'),      // ids 1-30
  ...makeRows(31, 'BBA'),      // ids 31-60
  ...makeRows(61, 'B.Tech')    // ids 61-90
])

/* ───────────── Reactive state & helpers ───────────── */
const courses            = ref<string[]>([])
const selectedCourse     = ref('All')
const courseDropdownOpen = ref(false)

const cities             = ref<string[]>([])
const selectedCities     = ref<string[]>([])
const dropdownOpen       = ref(false)
const searchQuery        = ref('')
const allSelected        = ref(false)

function rebuildCityLists (rows: Row[]) {
  const set = new Set<string>()
  rows.forEach(r => set.add(r.city))
  cities.value = Array.from(set)
  selectedCities.value = [...cities.value]
}
function initDropdowns () {
  const courseSet = new Set<string>()
  applications.value.forEach(a => courseSet.add(a.course))
  courses.value = ['All', ...Array.from(courseSet)]
  rebuildCityLists(applications.value)
}
initDropdowns()

const average = (arr: number[]) =>
  arr.length ? arr.reduce((s, v) => s + v, 0) / arr.length : 0

function selectCourse (course: string) {
  selectedCourse.value = course
  courseDropdownOpen.value = false
}

/* ---------------- watchers & filters ---------------- */
watch(selectedCourse, () => {
  rebuildCityLists(courseFilteredApps.value)
  allSelected.value = true
})
watch(allSelected, val => {
  selectedCities.value = val ? [...cities.value] : []
})

const courseFilteredApps = computed<Row[]>(() =>
  selectedCourse.value === 'All'
    ? applications.value
    : applications.value.filter(a => a.course === selectedCourse.value)
)

const filteredCities = computed(() =>
  cities.value.filter(c =>
    c.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

/* ---------------- aggregations ---------------- */
const cityWiseData = computed<Record<string, any>>(() => {
  const out: Record<string, any> = {}
  selectedCities.value.forEach(city => {
    const list = courseFilteredApps.value.filter(a => a.city === city)
    out[city] = {
      male:     list.filter(a => a.gender === 'Male').length,
      female:   list.filter(a => a.gender === 'Female').length,
      admitted: list.filter(a => a.status === 'Accepted').length,
      pending:  list.filter(a => a.status === 'Pending').length,
      rejected: list.filter(a => a.status === 'Rejected').length,
      scores: {
        admitted: average(list.filter(a => a.status === 'Accepted').map(a => a.score)),
        pending:  average(list.filter(a => a.status === 'Pending' ).map(a => a.score)),
        rejected: average(list.filter(a => a.status === 'Rejected').map(a => a.score))
      }
    }
  })
  return out
})

const filteredCityData = computed(() => {
  const labels   = []
  const admitted = []
  const pending  = []
  const rejected = []
  selectedCities.value.forEach(c => {
    const d = cityWiseData.value[c] || {}
    labels.push(c)
    admitted.push(d.admitted || 0)
    pending.push(d.pending || 0)
    rejected.push(d.rejected || 0)
  })
  return {
    labels,
    datasets: [
      { label: 'Admitted', data: admitted, backgroundColor: '#22c55e', stack: 's' },
      { label: 'Pending',  data: pending,  backgroundColor: '#facc15', stack: 's' },
      { label: 'Rejected', data: rejected, backgroundColor: '#ef4444', stack: 's' }
    ]
  }
})

const scoreBarData = computed(() => {
  const totals = { admitted: 0, pending: 0, rejected: 0 }
  const counts = { admitted: 0, pending: 0, rejected: 0 }
  selectedCities.value.forEach(c => {
    const d = cityWiseData.value[c] || {}
    totals.admitted += (d.scores?.admitted || 0) * (d.admitted || 0)
    counts.admitted += d.admitted || 0
    totals.pending  += (d.scores?.pending  || 0) * (d.pending  || 0)
    counts.pending  += d.pending  || 0
    totals.rejected += (d.scores?.rejected || 0) * (d.rejected || 0)
    counts.rejected += d.rejected || 0
  })
  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [{
      label: 'Average Score',
      data: [
        counts.admitted ? totals.admitted / counts.admitted : 0,
        counts.pending  ? totals.pending  / counts.pending  : 0,
        counts.rejected ? totals.rejected / counts.rejected : 0
      ],
      backgroundColor: ['#22c55e', '#facc15', '#ef4444']
    }]
  }
})

const pieData = computed(() => {
  let male = 0, female = 0
  selectedCities.value.forEach(c => {
    const d = cityWiseData.value[c] || {}
    male   += d.male   || 0
    female += d.female || 0
  })
  return {
    labels: ['Male', 'Female'],
    datasets: [{ data: [male, female], backgroundColor: ['#3b82f6', '#ec4899'] }]
  }
})

const statusPieData = computed(() => {
  let admitted = 0, pending = 0, rejected = 0
  selectedCities.value.forEach(c => {
    const d = cityWiseData.value[c] || {}
    admitted += d.admitted || 0
    pending  += d.pending  || 0
    rejected += d.rejected || 0
  })
  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [{
      data: [admitted, pending, rejected],
      backgroundColor: ['#22c55e', '#facc15', '#ef4444']
    }]
  }
})

/* ───────────── Chart options ───────────── */
const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title:  { display: true, text: 'Admission Status by City' }
  },
  scales: {
    x: { stacked: true },
    y: { stacked: true, beginAtZero: true }
  }
}
const scoreOptions = {
  ...barOptions,
  plugins: { ...barOptions.plugins, title: { display: true, text: 'Average Score by Status' } },
  scales: { y: { beginAtZero: true } }
}
</script>
