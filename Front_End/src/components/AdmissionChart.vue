<template>
  <div class="space-y-8 bg-gray-900 min-h-screen p-8">
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-10">
      <div class="text-indigo-400 text-lg">Loading admission data...</div>
    </div>

    <div v-else>
      <!-- Error State -->
      <div v-if="error" class="text-red-400 text-center mb-4">
        {{ error }}
      </div>

      <!-- Summary Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg">
          <h3 class="text-xl font-semibold text-indigo-300 mb-2">Total Applications</h3>
          <p class="text-3xl font-bold text-white">{{ filteredApplications.length }}</p>
        </div>
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg">
          <h3 class="text-xl font-semibold text-green-300 mb-2">Admitted</h3>
          <p class="text-3xl font-bold text-white">{{ admittedCount }}</p>
        </div>
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg">
          <h3 class="text-xl font-semibold text-yellow-300 mb-2">Pending</h3>
          <p class="text-3xl font-bold text-white">{{ pendingCount }}</p>
        </div>
        <div class="bg-gray-800 rounded-xl p-6 shadow-lg">
          <h3 class="text-xl font-semibold text-cyan-300 mb-2">Average Score</h3>
          <p class="text-3xl font-bold text-white">{{ averageScore }}</p>
        </div>
      </div>

      <!-- Filter Bar -->
      <div class="flex flex-wrap gap-4 mb-6">
        <div>
          <label class="text-gray-300 mr-2">Course:</label>
          <select v-model="selectedCourse" class="rounded p-2 bg-gray-700 text-white">
            <option value="">All</option>
            <option v-for="course in courseOptions" :key="course" :value="course">{{ course }}</option>
          </select>
        </div>
        <div>
          <label class="text-gray-300 mr-2">Gender:</label>
          <select v-model="selectedGender" class="rounded p-2 bg-gray-700 text-white">
            <option value="">All</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
        <button
          @click="resetFilters"
          class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded"
        >
          Reset Filters
        </button>
      </div>

      <!-- Chart Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Applications by City -->
        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg">
          <h3 class="text-lg font-semibold text-indigo-200 mb-2">Applications by City</h3>
          <Bar :data="cityBarData" :options="barOptions" />
        </div>

        <!-- Gender Distribution -->
        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg flex justify-center items-center">
          <Pie
            :data="genderPieData"
            :options="pieOptions"
            :height="200"
            :width="200"
          />
        </div>

        <!-- Status Distribution -->
        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg flex justify-center items-center">
          <Doughnut
            :data="statusDoughnutData"
            :options="pieOptions"
            :height="200"
            :width="200"
          />
        </div>

        <!-- Applications by Course -->
        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg">
          <h3 class="text-lg font-semibold text-cyan-200 mb-2">Applications by Course</h3>
          <Bar :data="courseBarData" :options="barOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Bar, Pie, Doughnut } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement)

/* ────────── STATE ────────── */
const applications = ref([])
const loading       = ref(true)
const error         = ref(null)

/* ────────── FILTERS ────────── */
const selectedCourse = ref('')
const selectedGender = ref('')

/* ────────── DATA FETCH ────────── */
const fetchData = async () => {
  loading.value = true
  error.value   = null
  try {
    const res = await fetch('http://localhost:8000/analytics')
    if (!res.ok) throw new Error('Failed to fetch analytics data')
    applications.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
onMounted(fetchData)

/* ────────── FILTERED LIST & OPTIONS ────────── */
const filteredApplications = computed(() =>
  applications.value.filter(app => {
    const courseOK = selectedCourse.value ? app.course_name === selectedCourse.value : true
    const genderOK = selectedGender.value ? app.gender === selectedGender.value : true
    return courseOK && genderOK
  })
)

const courseOptions = computed(() =>
  Array.from(new Set(applications.value.map(app => app.course_name)))
)

/* ────────── SUMMARY COUNTS (only these two lines edited) ────────── */
const admittedCount = computed(
  () => filteredApplications.value.filter(a => (a.status || '').toLowerCase() === 'accepted').length
)
const pendingCount  = computed(
  () => filteredApplications.value.filter(a => (a.status || '').toLowerCase() === 'pending').length
)

const averageScore  = computed(() => {
  const scores = filteredApplications.value
    .map(a => Number(a.score))
    .filter(s => !isNaN(s))
  return scores.length
    ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1)
    : 'N/A'
})

const resetFilters = () => {
  selectedCourse.value = ''
  selectedGender.value = ''
}

/* ────────── CHART DATA ────────── */
const cityBarData = computed(() => {
  const counts = {}
  filteredApplications.value.forEach(a => (counts[a.city] = (counts[a.city] || 0) + 1))
  return {
    labels: Object.keys(counts),
    datasets: [{ label: 'Applications', backgroundColor: '#6366f1', data: Object.values(counts) }]
  }
})

const genderPieData = computed(() => {
  const counts = { male: 0, female: 0 }
  filteredApplications.value.forEach(a => {
    const g = (a.gender || '').toLowerCase()
    if (g === 'male')   counts.male++
    if (g === 'female') counts.female++
  })
  return {
    labels: ['Male', 'Female'],
    datasets: [{ backgroundColor: ['#60a5fa', '#f472b6'], data: [counts.male, counts.female] }]
  }
})

const statusDoughnutData = computed(() => {
  const counts = { accepted: 0, pending: 0, rejected: 0 }
  filteredApplications.value.forEach(a => {
    const s = (a.status || '').toLowerCase()
    if (s === 'accepted') counts.accepted++
    if (s === 'pending')  counts.pending++
    if (s === 'rejected') counts.rejected++
  })
  return {
    labels: ['Accepted', 'Pending', 'Rejected'],
    datasets: [
      {
        backgroundColor: ['#34d399', '#fbbf24', '#f87171'],
        data: [counts.accepted, counts.pending, counts.rejected]
      }
    ]
  }
})

const courseBarData = computed(() => {
  const counts = {}
  filteredApplications.value.forEach(a => (counts[a.course_name] = (counts[a.course_name] || 0) + 1))
  return {
    labels: Object.keys(counts),
    datasets: [{ label: 'Applications', backgroundColor: '#06b6d4', data: Object.values(counts) }]
  }
})

/* ────────── CHART OPTIONS ────────── */
const barOptions = {
  responsive: true,
  plugins: { legend: { display: false }, title: { display: false } },
  scales: {
    x: { grid: { color: '#374151' }, ticks: { color: '#cbd5e1' } },
    y: { grid: { color: '#374151' }, ticks: { color: '#cbd5e1' } }
  }
}

/* circle charts: keep inside 200×200 canvas, legend at bottom */
const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: 5 },
  plugins: {
    legend: { position: 'bottom', labels: { color: '#cbd5e1', boxWidth: 12 } }
  }
}
</script>

<style scoped>
/* No extra styles needed */
</style>
