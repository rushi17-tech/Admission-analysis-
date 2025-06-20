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
import { ref, computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement, ArcElement)

const cities = ref(['Surat', 'Ahmedabad', 'Vadodara', 'Other'])
const selectedCities = ref([...cities.value])

const showMale = ref(true)
const showFemale = ref(true)

const cityWiseData = {
  Surat: { male: 40, female: 20 },
  Ahmedabad: { male: 25, female: 30 },
  Vadodara: { male: 15, female: 10 },
  Other: { male: 10, female: 15 }
}

// 📊 Bar chart data
const filteredCityData = computed(() => {
  const labels = []
  const male = []
  const female = []

  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    labels.push(city)
    male.push(showMale.value ? data.male : 0)
    female.push(showFemale.value ? data.female : 0)
  })

  return {
    labels,
    datasets: [
      {
        label: 'Male',
        data: male,
        backgroundColor: '#3b82f6'
      },
      {
        label: 'Female',
        data: female,
        backgroundColor: '#ec4899'
      }
    ]
  }
})

// 🍩 Pie chart data
const pieData = computed(() => {
  let totalMale = 0
  let totalFemale = 0
  selectedCities.value.forEach(city => {
    const data = cityWiseData[city]
    if (showMale.value) totalMale += data.male
    if (showFemale.value) totalFemale += data.female
  })

  return {
    labels: ['Male', 'Female'],
    datasets: [
      {
        data: [totalMale, totalFemale],
        backgroundColor: ['#3b82f6', '#ec4899']
      }
    ]
  }
})
</script>

<template>
  <div class="space-y-6">
    <!-- 🔘 Filters -->
    <div class="flex flex-wrap gap-4 items-center text-black">
      <div class="space-x-2">
        <label class="text-black"><input type="checkbox" v-model="showMale" /> Male</label>
        <label class="text-black"><input type="checkbox" v-model="showFemale" /> Female</label>
      </div>

      <div class="space-x-2">
        <span v-for="city in cities" :key="city">
          <label class="text-black">
            <input type="checkbox" :value="city" v-model="selectedCities" />
            {{ city }}
          </label>
        </span>
      </div>
    </div>

    <!-- 📊 Charts side by side -->
    <div class="flex flex-wrap gap-6 justify-center">
      <!-- 📈 Bar Chart -->
      <div class="bg-white p-4 rounded-xl shadow w-full md:w-[48%]">
        <h2 class="text-lg font-bold mb-2 text-gray-800 text-center">Admissions by City and Gender</h2>
        <div class="w-full h-64">
          <Bar :data="filteredCityData" :options="{ responsive: true, maintainAspectRatio: false }" />
        </div>
      </div>

      <!-- 🍩 Pie Chart Summary -->
      <div class="bg-white p-4 rounded-xl shadow w-full md:w-[48%]">
        <h2 class="text-lg font-bold mb-2 text-gray-800 text-center">Gender Summary</h2>
        <div class="w-full h-64">
          <Pie :data="pieData" :options="{ responsive: true, maintainAspectRatio: false }" />
        </div>
      </div>
    </div>
  </div>
</template>
