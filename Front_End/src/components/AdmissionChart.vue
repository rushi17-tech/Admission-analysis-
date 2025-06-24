<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement
} from 'chart.js'
import { Bar, Pie } from 'vue-chartjs'
import { ref, computed, watch } from 'vue'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement, ArcElement)

const cities = ref([
  'Surat', 'Ahmedabad', 'Vadodara', 'Rajkot', 'Gandhinagar',
  'Jamnagar', 'Bhavnagar', 'Junagadh', 'Nadiad', 'Other'
])

const selectedCities = ref([...cities.value.slice(0, 4)])
const dropdownOpen = ref(false)
const searchQuery = ref('')
const allSelected = ref(false)

const filteredCities = computed(() => {
  return cities.value.filter(city =>
    city.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

watch(allSelected, (val) => {
  selectedCities.value = val ? [...cities.value] : []
})

// ✨ Added average scores to each status
const cityWiseData = {
  Surat: { male: 40, female: 20, admitted: 30, pending: 20, rejected: 10, scores: { admitted: 85, pending: 65, rejected: 40 } },
  Ahmedabad: { male: 25, female: 30, admitted: 35, pending: 10, rejected: 10, scores: { admitted: 80, pending: 60, rejected: 50 } },
  Vadodara: { male: 15, female: 10, admitted: 15, pending: 5, rejected: 5, scores: { admitted: 82, pending: 55, rejected: 45 } },
  Rajkot: { male: 20, female: 15, admitted: 25, pending: 5, rejected: 5, scores: { admitted: 78, pending: 50, rejected: 40 } },
  Gandhinagar: { male: 18, female: 17, admitted: 20, pending: 10, rejected: 5, scores: { admitted: 83, pending: 60, rejected: 50 } },
  Jamnagar: { male: 10, female: 12, admitted: 10, pending: 8, rejected: 4, scores: { admitted: 75, pending: 55, rejected: 30 } },
  Bhavnagar: { male: 14, female: 16, admitted: 18, pending: 6, rejected: 6, scores: { admitted: 81, pending: 58, rejected: 42 } },
  Junagadh: { male: 12, female: 13, admitted: 15, pending: 5, rejected: 5, scores: { admitted: 77, pending: 52, rejected: 38 } },
  Nadiad: { male: 11, female: 9, admitted: 14, pending: 3, rejected: 3, scores: { admitted: 79, pending: 57, rejected: 41 } },
  Other: { male: 10, female: 15, admitted: 10, pending: 5, rejected: 10, scores: { admitted: 76, pending: 54, rejected: 35 } }
}

const filteredCityData = computed(() => {
  const labels = []
  const admitted = []
  const pending = []
  const rejected = []

  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    labels.push(city)
    admitted.push(data.admitted)
    pending.push(data.pending)
    rejected.push(data.rejected)
  })

  return {
    labels,
    datasets: [
      {
        label: 'Admitted',
        data: admitted,
        backgroundColor: '#22c55e',
        stack: 'status'
      },
      {
        label: 'Pending',
        data: pending,
        backgroundColor: '#facc15',
        stack: 'status'
      },
      {
        label: 'Rejected',
        data: rejected,
        backgroundColor: '#ef4444',
        stack: 'status'
      }
    ]
  }
})

// ✨ New bar chart for average scores
const scoreBarData = computed(() => {
  let totalAdmittedScore = 0, admittedCount = 0
  let totalPendingScore = 0, pendingCount = 0
  let totalRejectedScore = 0, rejectedCount = 0

  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    totalAdmittedScore += data.scores.admitted * data.admitted
    admittedCount += data.admitted

    totalPendingScore += data.scores.pending * data.pending
    pendingCount += data.pending

    totalRejectedScore += data.scores.rejected * data.rejected
    rejectedCount += data.rejected
  })

  const avgAdmitted = admittedCount ? totalAdmittedScore / admittedCount : 0
  const avgPending = pendingCount ? totalPendingScore / pendingCount : 0
  const avgRejected = rejectedCount ? totalRejectedScore / rejectedCount : 0

  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [
      {
        label: 'Average Score',
        data: [avgAdmitted, avgPending, avgRejected],
        backgroundColor: ['#22c55e', '#facc15', '#ef4444']
      }
    ]
  }
})

const pieData = computed(() => {
  let totalMale = 0, totalFemale = 0
  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    totalMale += data.male
    totalFemale += data.female
  })
  return {
    labels: ['Male', 'Female'],
    datasets: [{
      data: [totalMale, totalFemale],
      backgroundColor: ['#3b82f6', '#ec4899']
    }]
  }
})

const statusPieData = computed(() => {
  let totalAdmitted = 0, totalPending = 0, totalRejected = 0
  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    totalAdmitted += data.admitted
    totalPending += data.pending
    totalRejected += data.rejected
  })
  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [{
      data: [totalAdmitted, totalPending, totalRejected],
      backgroundColor: ['#22c55e', '#facc15', '#ef4444']
    }]
  }
})

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: {
      display: true,
      text: 'Admission Status by City'
    }
  },
  scales: {
    x: { stacked: true },
    y: { stacked: true, beginAtZero: true }
  }
}
</script>

<template>
  <div class="bg-white min-h-screen p-6 space-y-8 text-black">
    <!-- City Dropdown -->
    <div class="bg-white p-4 rounded-xl shadow space-y-4 relative">
      <h2 class="text-lg font-bold text-gray-800">Select Cities</h2>
      <div class="relative w-full md:w-1/2">
        <button
          @click="dropdownOpen = !dropdownOpen"
          class="w-full border px-4 py-2 text-left rounded-md bg-gray-50 hover:bg-gray-100"
        >
          {{ selectedCities.length ? selectedCities.join(', ') : 'Select cities' }}
        </button>
        <div v-if="dropdownOpen" class="absolute z-10 mt-1 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto p-2 space-y-2">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search cities..."
            class="w-full px-2 py-1 border rounded-md focus:outline-none"
          />
          <label class="flex items-center gap-2 px-1 py-1 text-sm font-medium">
            <input type="checkbox" v-model="allSelected" />
            Select All
          </label>
          <label
            v-for="city in filteredCities"
            :key="city"
            class="flex items-center gap-2 px-2 py-1 text-sm"
          >
            <input type="checkbox" :value="city" v-model="selectedCities" />
            {{ city }}
          </label>
        </div>
      </div>
    </div>

    <!-- Stacked Bar Chart -->
    <div class="bg-white p-6 rounded-xl shadow">
      <h2 class="text-xl font-bold mb-4 text-center text-gray-800">Admission Status by City</h2>
      <div class="w-full h-[500px]">
        <Bar :data="filteredCityData" :options="barOptions" />
      </div>
    </div>

    <!-- 3-Chart Layout -->
    <div class="flex flex-col md:flex-row gap-6 justify-center items-start">
      <!-- Gender Pie -->
      <div class="bg-white p-4 rounded-xl shadow w-full md:w-1/3">
        <h2 class="text-lg font-bold mb-2 text-center text-gray-800">Gender Summary</h2>
        <div class="w-full h-64">
          <Pie :data="pieData" :options="{ responsive: true, maintainAspectRatio: false }" />
        </div>
      </div>

      <!-- Average Score Bar -->
      <div class="bg-white p-4 rounded-xl shadow w-full md:w-1/3">
        <h2 class="text-lg font-bold mb-2 text-center text-gray-800">Avg Score by Status</h2>
        <div class="w-full h-64">
          <Bar :data="scoreBarData" :options="{ responsive: true, maintainAspectRatio: false }" />
        </div>
      </div>

      <!-- Admission Pie -->
      <div class="bg-white p-4 rounded-xl shadow w-full md:w-1/3">
        <h2 class="text-lg font-bold mb-2 text-center text-gray-800">Admission Summary</h2>
        <div class="w-full h-64">
          <Pie :data="statusPieData" :options="{ responsive: true, maintainAspectRatio: false }" />
        </div>
      </div>
    </div>
  </div>
</template>
