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
        <!-- School Filter with Checkboxes -->
        <div class="relative">
          <label class="text-gray-300 mr-2">School:</label>
          <button
            @click="showSchoolDropdown = !showSchoolDropdown"
            class="rounded p-2 bg-gray-700 text-white w-48 text-left"
          >
            {{ selectedSchools.length ? selectedSchools.join(', ') : 'All' }}
          </button>
          <div
            v-if="showSchoolDropdown"
            class="absolute bg-gray-800 z-50 mt-1 w-48 max-h-60 overflow-y-auto shadow-lg rounded p-2"
          >
            <div v-for="school in schools" :key="school" class="flex items-center space-x-2">
              <input
                type="checkbox"
                :value="school"
                v-model="selectedSchools"
                class="form-checkbox text-indigo-500"
              />
              <label class="text-white">{{ school }}</label>
            </div>
          </div>
        </div>

        <!-- Course Filter with Checkboxes -->
        <div class="relative">
          <label class="text-gray-300 mr-2">Course:</label>
          <button
            @click="showCourseDropdown = !showCourseDropdown"
            class="rounded p-2 bg-gray-700 text-white w-48 text-left"
          >
            {{ selectedCourses.length ? selectedCourses.join(', ') : 'All' }}
          </button>
          <div
            v-if="showCourseDropdown"
            class="absolute bg-gray-800 z-50 mt-1 w-48 max-h-60 overflow-y-auto shadow-lg rounded p-2"
          >
            <div v-for="course in courseOptions" :key="course" class="flex items-center space-x-2">
              <input
                type="checkbox"
                :value="course"
                v-model="selectedCourses"
                class="form-checkbox text-indigo-500"
              />
              <label class="text-white">{{ course }}</label>
            </div>
          </div>
        </div>

        <!-- City Filter with Checkboxes -->
        <div class="relative">
          <label class="text-gray-300 mr-2">City:</label>
          <button
            @click="showCityDropdown = !showCityDropdown"
            class="rounded p-2 bg-gray-700 text-white w-48 text-left"
          >
            {{ selectedCities.length ? selectedCities.join(', ') : 'All' }}
          </button>
          <div
            v-if="showCityDropdown"
            class="absolute bg-gray-800 z-50 mt-1 w-48 max-h-60 overflow-y-auto shadow-lg rounded p-2"
          >
            <div v-for="city in cityOptions" :key="city" class="flex items-center space-x-2">
              <input
                type="checkbox"
                :value="city"
                v-model="selectedCities"
                class="form-checkbox text-indigo-500"
              />
              <label class="text-white">{{ city }}</label>
            </div>
          </div>
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
        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg">
          <h3 class="text-lg font-semibold text-indigo-200 mb-2">Applications by City</h3>
          <Bar :data="cityBarData" :options="barOptions" />
        </div>

        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg flex justify-center items-center">
          <Pie :data="genderPieData" :options="pieOptions" :height="200" :width="200" />
        </div>

        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg flex justify-center items-center">
          <Doughnut :data="statusDoughnutData" :options="pieOptions" :height="200" :width="200" />
        </div>

        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg">
          <h3 class="text-lg font-semibold text-cyan-200 mb-2">Applications by Course</h3>
          <Bar :data="courseBarData" :options="barOptions" />
        </div>

        <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg">
          <h3 class="text-lg font-semibold text-emerald-200 mb-2">Applications by School</h3>
          <Bar :data="schoolBarData" :options="barOptions" />
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

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  ArcElement
)

const applications = ref([])
const schools = ref([])
const loading = ref(true)
const error = ref(null)

/* Filters */
const selectedSchools = ref([])
const selectedCourses = ref([])
const selectedCities = ref([])
const selectedGender = ref('')
const showSchoolDropdown = ref(false)
const showCourseDropdown = ref(false)
const showCityDropdown = ref(false)

const fetchData = async () => {
  loading.value = true
  error.value = null
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

const fetchSchools = async () => {
  try {
    const res = await fetch('http://localhost:8000/schools')
    if (!res.ok) throw new Error('Failed to fetch school list')
    schools.value = await res.json()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(() => {
  fetchData()
  fetchSchools()
})

const filteredApplications = computed(() =>
  applications.value.filter(app => {
    const schoolOK =
      selectedSchools.value.length > 0
        ? selectedSchools.value.includes(app.school_name)
        : true

    const courseOK =
      selectedCourses.value.length > 0
        ? selectedCourses.value.includes(app.course_name)
        : true

    const cityOK =
      selectedCities.value.length > 0
        ? selectedCities.value.includes(
            (app.city || '').trim().charAt(0).toUpperCase() +
              (app.city || '').trim().slice(1).toLowerCase()
          )
        : true

    const genderOK = selectedGender.value ? app.gender === selectedGender.value : true

    return schoolOK && courseOK && cityOK && genderOK
  })
)

const courseOptions = computed(() =>
  Array.from(new Set(applications.value.map(app => app.course_name)))
)

const cityOptions = computed(() =>
  Array.from(
    new Set(
      applications.value
        .map(app => (app.city || '').trim().toLowerCase())
        .filter(city => city)
    )
  ).map(city => city.charAt(0).toUpperCase() + city.slice(1))
)

const admittedCount = computed(() =>
  filteredApplications.value.filter(a => (a.status || '').toLowerCase() === 'accepted').length
)

const pendingCount = computed(() =>
  filteredApplications.value.filter(a => (a.status || '').toLowerCase() === 'pending').length
)

const averageScore = computed(() => {
  const scores = filteredApplications.value.map(a => Number(a.score)).filter(s => !isNaN(s))
  return scores.length
    ? (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1)
    : 'N/A'
})

const resetFilters = () => {
  selectedSchools.value = []
  selectedCourses.value = []
  selectedCities.value = []
  selectedGender.value = ''
}

/* Chart Data */
const cityBarData = computed(() => {
  const counts = {}
  filteredApplications.value.forEach(a => {
    const city = (a.city || '').trim().toLowerCase()
    if (city) counts[city] = (counts[city] || 0) + 1
  })
  const labels = Object.keys(counts).map(city => city.charAt(0).toUpperCase() + city.slice(1))
  return {
    labels,
    datasets: [
      {
        label: 'Applications',
        backgroundColor: '#6366f1',
        data: Object.values(counts)
      }
    ]
  }
})

const genderPieData = computed(() => {
  const counts = { male: 0, female: 0 }
  filteredApplications.value.forEach(a => {
    const g = (a.gender || '').toLowerCase()
    if (g === 'male') counts.male++
    if (g === 'female') counts.female++
  })
  return {
    labels: ['Male', 'Female'],
    datasets: [
      {
        backgroundColor: ['#60a5fa', '#f472b6'],
        data: [counts.male, counts.female]
      }
    ]
  }
})

const statusDoughnutData = computed(() => {
  const counts = { accepted: 0, pending: 0, rejected: 0 }
  filteredApplications.value.forEach(a => {
    const s = (a.status || '').toLowerCase()
    if (s === 'accepted') counts.accepted++
    if (s === 'pending') counts.pending++
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
  filteredApplications.value.forEach(a => {
    counts[a.course_name] = (counts[a.course_name] || 0) + 1
  })
  return {
    labels: Object.keys(counts),
    datasets: [
      {
        label: 'Applications',
        backgroundColor: '#06b6d4',
        data: Object.values(counts)
      }
    ]
  }
})

const schoolBarData = computed(() => {
  const counts = {}
  filteredApplications.value.forEach(a => {
    counts[a.school_name] = (counts[a.school_name] || 0) + 1
  })
  return {
    labels: Object.keys(counts),
    datasets: [
      {
        label: 'Applications',
        backgroundColor: '#34d399',
        data: Object.values(counts)
      }
    ]
  }
})

const barOptions = {
  responsive: true,
  plugins: { legend: { display: false }, title: { display: false } },
  scales: {
    x: { grid: { color: '#374151' }, ticks: { color: '#cbd5e1' } },
    y: { grid: { color: '#374151' }, ticks: { color: '#cbd5e1' } }
  }
}

const pieOptions = {
  responsive: true,
  maintainAspectRatio: false,
  layout: { padding: 5 },
  plugins: {
    legend: { position: 'bottom', labels: { color: '#cbd5e1', boxWidth: 12 } }
  }
}
</script>
