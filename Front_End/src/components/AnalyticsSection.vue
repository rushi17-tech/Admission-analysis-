<!-- src/components/Analytics.vue -->
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

/* raw data */
const raw = ref<Row[]>([])

/* filters */
const search = ref('')
const course = ref('')
const status = ref('')

const courseOptions = computed(() => [...new Set(raw.value.map(r => r.course_name))])
const statusOptions = ['pending', 'accepted', 'rejected']

/* filtered list */
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

/* fetch */
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
  <div class="relative py-10 px-3 md:px-10 min-h-[82vh] animate-fade-in text-white">
    <!-- heading -->
    <h3 class="page-heading mb-10 text-4xl font-extrabold tracking-wide">
      Admission&nbsp;Analytics
    </h3>

    <!-- filters -->
    <div
      class="glass-filter flex flex-wrap gap-6 items-end mb-10 p-6 rounded-2xl"
    >
      <div>
        <label class="filter-label">Search</label>
        <input
          v-model="search"
          type="text"
          placeholder="student or course…"
          class="filter-input w-56"
        />
      </div>

      <div>
        <label class="filter-label">Course</label>
        <select v-model="course" class="filter-input w-44">
          <option value="">All</option>
          <option v-for="c in courseOptions" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div>
        <label class="filter-label">Status</label>
        <select v-model="status" class="filter-input w-36">
          <option value="">All</option>
          <option v-for="s in statusOptions" :key="s" :value="s">
            {{ s.charAt(0).toUpperCase() + s.slice(1) }}
          </option>
        </select>
      </div>
    </div>

    <!-- table -->
    <div class="glass-table overflow-x-auto rounded-2xl">
      <table class="w-full text-sm text-gray-200">
        <thead class="sticky top-0 bg-slate-800/70 backdrop-blur">
          <tr class="text-left">
            <th class="tbl-th">ID</th>
            <th class="tbl-th">Student</th>
            <th class="tbl-th">Course</th>
            <th class="tbl-th">Status</th>
            <th class="tbl-th text-center">Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in analytics" :key="item.id" class="hover:bg-slate-700/30">
            <td class="tbl-td text-center">{{ item.id }}</td>
            <td class="tbl-td">{{ item.student_name }}</td>
            <td class="tbl-td">{{ item.course_name }}</td>
            <td class="tbl-td capitalize">
              <span
                :class="{
                  'text-amber-400': item.status === 'pending',
                  'text-cyan-400': item.status === 'accepted',
                  'text-rose-400': item.status === 'rejected'
                }"
              >
                {{ item.status }}
              </span>
            </td>
            <td class="tbl-td text-center">{{ item.score ?? 'N/A' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
/* blurred heading */
.page-heading{
  @apply inline-block px-6 py-3 rounded-2xl;
  background: rgba(17,24,39,0.55);
  backdrop-filter: blur(14px) saturate(160%);
}

/* glass filter bar */
.glass-filter{
  background: rgba(17,24,39,0.55);
  backdrop-filter: blur(18px) saturate(160%);
  border: 1.5px solid rgba(255,255,255,0.12);
  box-shadow: 0 4px 24px rgba(74,222,255,.12);
}
.filter-label{ @apply block text-sm mb-1 text-gray-300; }
.filter-input{
  @apply bg-transparent border border-gray-500 rounded-md px-3 py-1.5 outline-none focus:ring-2 focus:ring-indigo-500;
}

/* glass table */
.glass-table{
  background: rgba(17,24,39,0.55);
  backdrop-filter: blur(18px) saturate(160%);
  border: 1.5px solid rgba(255,255,255,0.1);
  box-shadow: 0 6px 32px rgba(74,222,255,0.15),
              0 1.5px 8px rgba(139,92,246,0.15);
}
.tbl-th{
  @apply px-4 py-2 font-semibold text-gray-100 border-b border-slate-600;
}
.tbl-td{
  @apply px-4 py-2 border-b border-slate-700;
}

/* fade animation */
.fade-enter-active,.fade-leave-active{ transition:opacity .3s; }
.fade-enter-from,.fade-leave-to{ opacity:0; }
@keyframes fadeIn{ from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0);} }
.animate-fade-in{ animation:fadeIn .6s ease forwards; }
</style>
