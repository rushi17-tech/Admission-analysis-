<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Row {
  id: number
  student_name: string
  course_name: string
  status: string
  score: number | null
}

const BASE_URL = 'http://localhost:8000/api'

/* raw data from backend */
const raw = ref<Row[]>([])

/* local filters */
const search = ref('')
const course = ref('')
const status = ref('')

/* derived lists for the filter dropdowns */
const courseOptions = computed(() => [...new Set(raw.value.map(r => r.course_name))])
const statusOptions = ['pending', 'accepted', 'rejected']

/* filtered list for the table */
const analytics = computed(() =>
  raw.value.filter(r => {
    const q = search.value.trim().toLowerCase()
    const okSearch =
      !q ||
      r.student_name.toLowerCase().includes(q) ||
      r.course_name .toLowerCase().includes(q)
    const okCourse = !course.value || r.course_name === course.value
    const okStatus = !status.value || r.status === status.value
    return okSearch && okCourse && okStatus
  })
)

/* fetch once when mounted */
onMounted(async () => {
  try {
    const { data } = await axios.get<Row[]>(`${BASE_URL}/analytics`)
    raw.value = data
  } catch (e) {
    console.error('Failed to load analytics:', e)
  }
})
</script>

<template>
  <div class="space-y-6">
    <h3 class="text-2xl font-bold text-gray-800">Admission&nbsp;Analytics</h3>

    <!-- Filters -->
    <div class="flex flex-wrap gap-4 items-end">
      <div>
        <label class="block text-sm mb-1 text-gray-600">Search</label>
        <input
          v-model="search"
          type="text"
          placeholder="student or course…"
          class="border rounded-md px-3 py-1.5 w-56"
        />
      </div>

      <div>
        <label class="block text-sm mb-1 text-gray-600">Course</label>
        <select v-model="course" class="border rounded-md px-3 py-1.5 w-44">
          <option value="">All</option>
          <option v-for="c in courseOptions" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm mb-1 text-gray-600">Status</label>
        <select v-model="status" class="border rounded-md px-3 py-1.5 w-36">
          <option value="">All</option>
          <option v-for="s in statusOptions" :key="s" :value="s">
            {{ s.charAt(0).toUpperCase() + s.slice(1) }}
          </option>
        </select>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-xl shadow-md overflow-x-auto">
      <table class="w-full border text-sm text-gray-900">
        <thead class="bg-gray-100">
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
            <td class="p-2 border capitalize">{{ item.status }}</td>
            <td class="p-2 border text-center">{{ item.score ?? 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
