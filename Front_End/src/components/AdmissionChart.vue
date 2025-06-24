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
import { ref, computed, watch, onMounted } from 'vue'
import axios from 'axios'

ChartJS.register(Title, Tooltip, Legend, CategoryScale, LinearScale, BarElement, ArcElement)

const applications = ref([])
const cities = ref([])
const selectedCities = ref([])
const dropdownOpen = ref(false)
const searchQuery = ref('')
const allSelected = ref(false)

const fetchApplications = async () => {
  try {
    const res = await axios.get("http://localhost:8000/applications")
    applications.value = res.data

    // Extract unique cities from application data
    const citySet = new Set()
    res.data.forEach(app => {
      if (app.city) citySet.add(app.city)
    })
    cities.value = Array.from(citySet)
    selectedCities.value = [...cities.value.slice(0, 4)]
  } catch (err) {
    console.error("Failed to fetch applications:", err)
  }
}

onMounted(() => {
  fetchApplications()
})

const filteredCities = computed(() => {
  return cities.value.filter(city =>
    city.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

watch(allSelected, (val) => {
  selectedCities.value = val ? [...cities.value] : []
})

const cityWiseData = computed(() => {
  const data = {}
  selectedCities.value.forEach(city => {
    const filtered = applications.value.filter(app => app.city === city)
    data[city] = {
      male: filtered.filter(a => a.gender === 'Male').length,
      female: filtered.filter(a => a.gender === 'Female').length,
      admitted: filtered.filter(a => a.status === 'Accepted').length,
      pending: filtered.filter(a => a.status === 'Pending').length,
      rejected: filtered.filter(a => a.status === 'Rejected').length,
      scores: {
        admitted: average(filtered.filter(a => a.status === 'Accepted').map(a => a.score)),
        pending: average(filtered.filter(a => a.status === 'Pending').map(a => a.score)),
        rejected: average(filtered.filter(a => a.status === 'Rejected').map(a => a.score))
      }
    }
  })
  return data
})

function average(arr) {
  if (!arr.length) return 0
  return arr.reduce((sum, v) => sum + v, 0) / arr.length
}

const filteredCityData = computed(() => {
  const labels = []
  const admitted = []
  const pending = []
  const rejected = []

  for (const city of selectedCities.value) {
    const data = cityWiseData.value[city] || {}
    labels.push(city)
    admitted.push(data.admitted || 0)
    pending.push(data.pending || 0)
    rejected.push(data.rejected || 0)
  }

  return {
    labels,
    datasets: [
      { label: 'Admitted', data: admitted, backgroundColor: '#22c55e', stack: 'status' },
      { label: 'Pending', data: pending, backgroundColor: '#facc15', stack: 'status' },
      { label: 'Rejected', data: rejected, backgroundColor: '#ef4444', stack: 'status' }
    ]
  }
})

const scoreBarData = computed(() => {
  let totalAdmitted = 0, countAdmitted = 0
  let totalPending = 0, countPending = 0
  let totalRejected = 0, countRejected = 0

  selectedCities.value.forEach(city => {
    const scores = cityWiseData.value[city]?.scores || {}
    const counts = cityWiseData.value[city] || {}

    totalAdmitted += scores.admitted * (counts.admitted || 0)
    countAdmitted += counts.admitted || 0

    totalPending += scores.pending * (counts.pending || 0)
    countPending += counts.pending || 0

    totalRejected += scores.rejected * (counts.rejected || 0)
    countRejected += counts.rejected || 0
  })

  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [
      {
        label: 'Average Score',
        data: [
          countAdmitted ? totalAdmitted / countAdmitted : 0,
          countPending ? totalPending / countPending : 0,
          countRejected ? totalRejected / countRejected : 0
        ],
        backgroundColor: ['#22c55e', '#facc15', '#ef4444']
      }
    ]
  }
})

const pieData = computed(() => {
  let male = 0, female = 0
  selectedCities.value.forEach(city => {
    const data = cityWiseData.value[city] || {}
    male += data.male || 0
    female += data.female || 0
  })
  return {
    labels: ['Male', 'Female'],
    datasets: [{
      data: [male, female],
      backgroundColor: ['#3b82f6', '#ec4899']
    }]
  }
})

const statusPieData = computed(() => {
  let admitted = 0, pending = 0, rejected = 0
  selectedCities.value.forEach(city => {
    const data = cityWiseData.value[city] || {}
    admitted += data.admitted || 0
    pending += data.pending || 0
    rejected += data.rejected || 0
  })
  return {
    labels: ['Admitted', 'Pending', 'Rejected'],
    datasets: [{
      data: [admitted, pending, rejected],
      backgroundColor: ['#22c55e', '#facc15', '#ef4444']
    }]
  }
})

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { position: 'top' },
    title: { display: true, text: 'Admission Status by City' }
  },
  scales: {
    x: { stacked: true },
    y: { stacked: true, beginAtZero: true }
  }
}
</script>
