<template>
  <div class="space-y-8 bg-gray-900 min-h-screen p-8">
    <!-- ────────── SUMMARY SECTION ────────── -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-gray-800 rounded-xl p-6 shadow-lg transform hover:scale-105 transition-transform duration-300">
        <h3 class="text-xl font-semibold text-indigo-300 mb-2">Total Applications</h3>
        <p class="text-3xl font-bold text-white">{{ totalApplications }}</p>
      </div>
      <div class="bg-gray-800 rounded-xl p-6 shadow-lg transform hover:scale-105 transition-transform duration-300">
        <h3 class="text-xl font-semibold text-emerald-300 mb-2">Admitted</h3>
        <p class="text-3xl font-bold text-white">{{ admitted }}</p>
      </div>
      <div class="bg-gray-800 rounded-xl p-6 shadow-lg transform hover:scale-105 transition-transform duration-300">
        <h3 class="text-xl font-semibold text-pink-300 mb-2">Pending</h3>
        <p class="text-3xl font-bold text-white">{{ pending }}</p>
      </div>
      <div class="bg-gray-800 rounded-xl p-6 shadow-lg transform hover:scale-105 transition-transform duration-300">
        <h3 class="text-xl font-semibold text-cyan-300 mb-2">Avg Score</h3>
        <p class="text-3xl font-bold text-white">{{ avgScore }}</p>
      </div>
    </div>

    <!-- ────────── FILTER BAR ────────── -->
    <div class="flex flex-wrap gap-4 mb-8">
      <!-- Course filter -->
      <div class="relative">
        <button
          class="px-4 py-2 bg-indigo-700 text-white rounded-lg shadow hover:bg-indigo-600 transition-colors"
          @click="courseDropdownOpen = !courseDropdownOpen"
        >
          Courses ({{ selectedCourses.length }}) ▾
        </button>
        <div
          v-if="courseDropdownOpen"
          class="absolute z-10 mt-2 w-56 bg-gray-800 border border-gray-700 rounded-lg shadow-lg p-4"
        >
          <input
            v-model="courseSearch"
            type="text"
            placeholder="Search course…"
            class="w-full mb-3 px-2 py-1 border rounded bg-gray-900 text-gray-100 border-gray-700 focus:ring-2 focus:ring-indigo-500"
          />
          <label class="flex items-center mb-2 text-gray-200">
            <input type="checkbox" v-model="allCoursesSelected" class="mr-2 rounded" />
            Select all
          </label>
          <div class="h-40 overflow-y-auto pr-2 custom-scroll">
            <label
              v-for="course in filteredCourses"
              :key="course"
              class="flex items-center mb-1 cursor-pointer text-gray-200 hover:text-indigo-300"
            >
              <input
                type="checkbox"
                :value="course"
                v-model="selectedCourses"
                class="mr-2 rounded"
              />
              {{ course }}
            </label>
          </div>
        </div>
      </div>

      <!-- City filter -->
      <div class="relative">
        <button
          class="px-4 py-2 bg-emerald-700 text-white rounded-lg shadow hover:bg-emerald-600 transition-colors"
          @click="cityDropdownOpen = !cityDropdownOpen"
        >
          Cities ({{ selectedCities.length }}) ▾
        </button>
        <div
          v-if="cityDropdownOpen"
          class="absolute z-10 mt-2 w-60 bg-gray-800 border border-gray-700 rounded-lg shadow-lg p-4"
        >
          <input
            v-model="citySearch"
            type="text"
            placeholder="Search city…"
            class="w-full mb-3 px-2 py-1 border rounded bg-gray-900 text-gray-100 border-gray-700 focus:ring-2 focus:ring-emerald-500"
          />
          <label class="flex items-center mb-2 text-gray-200">
            <input type="checkbox" v-model="allCitiesSelected" class="mr-2 rounded" />
            Select all
          </label>
          <div class="h-40 overflow-y-auto pr-2 custom-scroll">
            <label
              v-for="city in filteredCities"
              :key="city"
              class="flex items-center mb-1 cursor-pointer text-gray-200 hover:text-emerald-300"
            >
              <input
                type="checkbox"
                :value="city"
                v-model="selectedCities"
                class="mr-2 rounded"
              />
              {{ city }}
            </label>
          </div>
        </div>
      </div>

      <!-- Year filter -->
      <div class="relative">
        <button
          class="px-4 py-2 bg-pink-700 text-white rounded-lg shadow hover:bg-pink-600 transition-colors"
          @click="yearDropdownOpen = !yearDropdownOpen"
        >
          Year: {{ selectedYear === 'All' ? 'All' : selectedYear }}
        </button>
        <div
          v-if="yearDropdownOpen"
          class="absolute z-10 mt-2 w-36 bg-gray-800 border border-gray-700 rounded-lg shadow-lg custom-scroll"
        >
          <ul>
            <li
              v-for="year in years"
              :key="year"
              @click="selectYear(year)"
              class="px-4 py-2 hover:bg-pink-900 cursor-pointer text-gray-100 hover:text-pink-300 transition-colors"
            >
              {{ year }}
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- ────────── CHART GRID ────────── -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg transform hover:scale-[1.01] transition-transform duration-300">
        <Bar :data="filteredCityData" :options="barOptions" />
      </div>
      <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg transform hover:scale-[1.01] transition-transform duration-300">
        <Pie :data="scorePieData" :options="pieOptions" />
      </div>
      <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg transform hover:scale-[1.01] transition-transform duration-300">
        <Doughnut :data="genderDoughnutData" :options="doughnutOptions" />
      </div>
      <div class="h-[400px] bg-gray-800 rounded-xl p-4 shadow-lg transform hover:scale-[1.01] transition-transform duration-300">
        <Radar :data="radarData" :options="radarOptions" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Chart as ChartJS,
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  BarElement, ArcElement, RadialLinearScale, PointElement, LineElement,
  Filler
} from 'chart.js'
import { Bar, Pie, Doughnut, Radar } from 'vue-chartjs'
import { ref, computed, watch } from 'vue'

ChartJS.register(
  Title, Tooltip, Legend,
  CategoryScale, LinearScale,
  BarElement, ArcElement,
  RadialLinearScale, PointElement, LineElement,
  Filler
)

type Row = {
  id: number
  course: string
  city: string
  gender: 'Male' | 'Female'
  status: 'Accepted' | 'Pending' | 'Rejected'
  score: number
  year: number
}

const CITIES = [
  'Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar',
  'Bharuch', 'Jamnagar', 'Bhavnagar', 'Junagadh', 'Navsari'
]
const COURSES = ['BCA', 'BBA', 'B.Tech', 'B.Com', 'MBA']
const YEARS = [2022, 2023, 2024, 2025]

function randomScore(status: string) {
  if (status === 'Accepted') return 75 + Math.floor(Math.random() * 20)
  if (status === 'Pending') return 60 + Math.floor(Math.random() * 20)
  return 40 + Math.floor(Math.random() * 25)
}
function makeRows(): Row[] {
  let id = 1
  const rows: Row[] = []
  for (const year of YEARS) {
    for (const course of COURSES) {
      for (const city of CITIES) {
        ['Accepted', 'Pending', 'Rejected'].forEach((status, i) => {
          rows.push(
            {
              id: id++,
              course,
              city,
              gender: i % 2 === 0 ? 'Male' : 'Female',
              status: status as Row['status'],
              score: randomScore(status),
              year
            },
            {
              id: id++,
              course,
              city,
              gender: i % 2 === 0 ? 'Female' : 'Male',
              status: status as Row['status'],
              score: randomScore(status),
              year
            }
          )
        })
      }
    }
  }
  return rows
}
const applications = ref<Row[]>(makeRows())

// Filters & State
const courses = ref<string[]>([...COURSES])
const selectedCourses = ref<string[]>([...COURSES])
const courseDropdownOpen = ref(false)
const courseSearch = ref('')
const allCoursesSelected = ref(true)

const cities = ref<string[]>([...CITIES])
const selectedCities = ref<string[]>([...CITIES])
const cityDropdownOpen = ref(false)
const citySearch = ref('')
const allCitiesSelected = ref(true)

const years = ref<(number | 'All')[]>(['All', ...YEARS])
const selectedYear = ref<'All' | number>('All')
const yearDropdownOpen = ref(false)

function selectYear(year: number | 'All') {
  selectedYear.value = year
  yearDropdownOpen.value = false
}

watch(allCoursesSelected, val => {
  selectedCourses.value = val ? [...courses.value] : []
})
watch(allCitiesSelected, val => {
  selectedCities.value = val ? [...cities.value] : []
})

const filteredCourses = computed(() =>
  courses.value.filter(c =>
    c.toLowerCase().includes(courseSearch.value.toLowerCase())
  )
)
const filteredCities = computed(() =>
  cities.value.filter(c =>
    c.toLowerCase().includes(citySearch.value.toLowerCase())
  )
)

// Filtered Data
const filteredApps = computed<Row[]>(() =>
  applications.value.filter(a =>
    selectedCourses.value.includes(a.course) &&
    selectedCities.value.includes(a.city) &&
    (selectedYear.value === 'All' || a.year === selectedYear.value)
  )
)

// Summary Stats
const totalApplications = computed(() => filteredApps.value.length)
const admitted = computed(() => filteredApps.value.filter(a => a.status === 'Accepted').length)
const pending = computed(() => filteredApps.value.filter(a => a.status === 'Pending').length)
const avgScore = computed(() => {
  const sum = filteredApps.value.reduce((s, v) => s + v.score, 0)
  return filteredApps.value.length ? Math.round(sum / filteredApps.value.length) : 0
})

// Chart Data
const cityWiseData = computed(() => {
  const out: Record<string, any> = {}
  selectedCities.value.forEach(city => {
    const list = filteredApps.value.filter(a => a.city === city)
    out[city] = {
      admitted: list.filter(a => a.status === 'Accepted').length,
      pending: list.filter(a => a.status === 'Pending').length,
      rejected: list.filter(a => a.status === 'Rejected').length,
      avgScore: list.length
        ? Math.round(list.reduce((sum, a) => sum + a.score, 0) / list.length)
        : 0
    }
  })
  return out
})

const filteredCityData = computed(() => {
  const labels = []
  const admitted = []
  const pending = []
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
      { label: 'Admitted', data: admitted, backgroundColor: '#22d3ee', stack: 's', borderColor: '#06b6d4', borderWidth: 1 },
      { label: 'Pending', data: pending, backgroundColor: '#f472b6', stack: 's', borderColor: '#ec4899', borderWidth: 1 },
      { label: 'Rejected', data: rejected, backgroundColor: '#f87171', stack: 's', borderColor: '#ef4444', borderWidth: 1 }
    ]
  }
})

const scorePieData = computed(() => {
  const admitted = filteredApps.value.filter(a => a.status === 'Accepted')
  const pending = filteredApps.value.filter(a => a.status === 'Pending')
  const rejected = filteredApps.value.filter(a => a.status === 'Rejected')
  const avg = arr => arr.length ? Math.round(arr.reduce((s, v) => s + v.score, 0) / arr.length) : 0
  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [{
      data: [avg(admitted), avg(pending), avg(rejected)],
      backgroundColor: ['#06b6d4', '#a21caf', '#dc2626'],
      borderColor: ['#0891b2', '#9d174d', '#b91c1c'],
      borderWidth: 1
    }]
  }
})

const genderDoughnutData = computed(() => {
  const male = filteredApps.value.filter(a => a.gender === 'Male').length
  const female = filteredApps.value.filter(a => a.gender === 'Female').length
  return {
    labels: ['Male', 'Female'],
    datasets: [{
      data: [male, female],
      backgroundColor: ['#6366f1', '#f472b6'],
      borderColor: ['#4f46e5', '#ec4899'],
      borderWidth: 1
    }]
  }
})

const radarData = computed(() => {
  const courseLabels = selectedCourses.value
  const data = courseLabels.map(course => {
    const arr = filteredApps.value.filter(a => a.course === course)
    return arr.length ? Math.round(arr.reduce((s, a) => s + a.score, 0) / arr.length) : 0
  })
  return {
    labels: courseLabels,
    datasets: [{
      label: 'Avg Score by Course',
      data,
      backgroundColor: 'rgba(34,211,238,0.2)',
      borderColor: '#22d3ee',
      pointBackgroundColor: '#a21caf',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: '#a21caf',
      fill: true
    }]
  }
})

// Chart Options
const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top', labels: { font: { size: 14 }, color: '#fff' } },
    title: { display: true, text: 'Admission Status by City', font: { size: 16 }, color: '#fff' }
  },
  scales: {
    x: { stacked: true, ticks: { color: '#fff' }, grid: { color: '#444' } },
    y: { stacked: true, beginAtZero: true, ticks: { color: '#fff' }, grid: { color: '#444' } }
  },
  animation: {
    duration: 1000,
    easing: 'easeInOutQuart'
  }
}

const pieOptions = {
  plugins: {
    legend: { labels: { font: { size: 14 }, color: '#fff' } },
    title: { display: true, text: 'Avg Score by Status', font: { size: 16 }, color: '#fff' }
  },
  animation: {
    duration: 1000,
    easing: 'easeInOutQuart'
  }
}

const doughnutOptions = {
  plugins: {
    legend: { labels: { font: { size: 14 }, color: '#fff' } },
    title: { display: true, text: 'Gender Distribution', font: { size: 16 }, color: '#fff' }
  },
  animation: {
    duration: 1000,
    easing: 'easeInOutQuart'
  }
}

const radarOptions = {
  plugins: {
    legend: { labels: { font: { size: 14 }, color: '#fff' } },
    title: { display: true, text: 'Avg Score by Course', font: { size: 16 }, color: '#fff' }
  },
  scales: {
    r: {
      angleLines: { color: '#888' },
      grid: { color: '#444' },
      pointLabels: { color: '#fff', font: { size: 12 } },
      ticks: { color: '#fff', backdropColor: 'transparent' }
    }
  },
  animation: {
    duration: 1000,
    easing: 'easeInOutQuart'
  }
}
</script>

<style>
.custom-scroll::-webkit-scrollbar {
  width: 6px;
}
.custom-scroll::-webkit-scrollbar-track {
  background: #2d3748;
  border-radius: 3px;
}
.custom-scroll::-webkit-scrollbar-thumb {
  background: #4a5568;
  border-radius: 3px;
}
.custom-scroll::-webkit-scrollbar-thumb:hover {
  background: #718096;
}
</style>
