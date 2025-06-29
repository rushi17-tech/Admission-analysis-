<template>
  <!-- show this page only when the Applications tab is active -->
  <div v-if="activeTab === 'applications'" class="p-6 min-h-screen bg-black text-white">
    <!-- ────────── PAGE TITLE ────────── -->
    <h3
      class="text-4xl font-extrabold mb-10 flex items-center gap-3"
    >
      <svg class="w-10 h-10 text-cyan-400" fill="none" stroke="currentColor" stroke-width="2"
           viewBox="0 0 24 24">
        <path d="M12 4v16m8-8H4" />
      </svg>
      Applications Overview
    </h3>


    <!-- ────────── FLIP‑CARDS GRID ────────── -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
      <!-- CARD 0 — NEW APPLICATIONS -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card">
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-cyan-400">
            <svg class="w-12 h-12 text-cyan-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
                 viewBox="0 0 24 24">
              <path d="M16 21v-2a4 4 0 00-3-3.87M6 21v-2a4 4 0 013-3.87m6-7a4 4 0 11-8 0 4 4 0 018 0zm6 4v6m3-3h-6" />
            </svg>
            <h4 class="text-2xl font-bold text-white mb-2">New Applications</h4>
            <span class="text-6xl font-extrabold mb-4 text-cyan-400">
              {{ analytics.length }}
            </span>
            <button
              class="mt-4 px-6 py-2 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="openModal('all')"
            >
              Show Details
            </button>
          </div>
        </div>
      </div>

      <!-- CARD 1 — DOCUMENTS PENDING -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card" :class="{ flipped: flippedCard === 1 }">
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-amber-400">
            <svg class="w-12 h-12 text-amber-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
                 viewBox="0 0 24 24">
              <path d="M7 7h10M7 11h10M7 15h6M5 19h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h4 class="text-2xl font-bold text-white mb-2">Documents Pending</h4>
            <span class="text-6xl font-extrabold mb-4 text-amber-400">
              {{ pendingCount }}
            </span>
            <button
              class="mt-4 px-6 py-2 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="flipCard(1)"
            >
              Show Details
            </button>
          </div>

          <!-- BACK -->
          <div class="flip-card-back glassmorphic-card border-amber-400">
            <h4 class="text-xl font-semibold text-white mb-2">Details</h4>
            <ul class="text-base text-gray-300 text-center space-y-1 mb-4">
              <li><b>{{ pendingCount }}</b> applications require additional documentation.</li>
              <li v-if="pendingCount === 0">Great news — nothing is pending!</li>
              <li v-else>Click below for the full list.</li>
            </ul>
            <button
              class="mb-2 px-5 py-1 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="openModal('pending')"
            >
              View More
            </button>
            <button
              class="mt-2 px-6 py-2 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="flipCard(-1)"
            >
              Back
            </button>
          </div>
        </div>
      </div>

      <!-- CARD 2 — REJECTED -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card" :class="{ flipped: flippedCard === 2 }">
          <!-- FRONT -->
          <div class="flip-card-front glassmorphic-card border-rose-400">
            <svg class="w-12 h-12 text-rose-400 mb-3" fill="none" stroke="currentColor" stroke-width="2"
                 viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" />
              <line x1="4" y1="4" x2="20" y2="20" />
            </svg>
            <h4 class="text-2xl font-bold text-white mb-2">Rejected Applications</h4>
            <span class="text-6xl font-extrabold mb-4 text-rose-400">
              {{ rejectedCount }}
            </span>
            <button
              class="mt-4 px-6 py-2 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="flipCard(2)"
            >
              Show Details
            </button>
          </div>

          <!-- BACK -->
          <div class="flip-card-back glassmorphic-card border-rose-400">
            <h4 class="text-xl font-semibold text-white mb-2">Details</h4>
            <ul class="text-base text-gray-300 text-center space-y-1 mb-4">
              <li><b>{{ rejectedCount }}</b> applications have been rejected.</li>
              <li v-if="rejectedCount === 0">No rejections 🎉</li>
              <li v-else>Click below for the full list.</li>
            </ul>
            <button
              class="mb-2 px-5 py-1 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="openModal('rejected')"
            >
              View More
            </button>
            <button
              class="mt-2 px-6 py-2 bg-gray-800/80 border border-gray-600 rounded-full shadow hover:scale-105 transition"
              @click="flipCard(-1)"
            >
              Back
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- ────────── MODAL ────────── -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur">
      <div
        class="bg-gray-900/90 border-2 border-gray-700 rounded-2xl p-8 shadow-2xl w-full max-w-xl"
      >
        <h4 class="text-2xl font-bold text-white mb-4">
          {{
            modalType === 'all'
              ? 'All Applications'
              : modalType === 'pending'
              ? 'Pending Applications'
              : 'Rejected Applications'
          }}
        </h4>

        <!-- Loading state -->
        <p v-if="isLoadingModal" class="text-center text-white">Loading…</p>
        <ul v-else class="space-y-3 h-96 overflow-y-auto pr-2">
          <li
            v-for="item in modalData"
            :key="item.application_id"
            class="flex flex-col bg-gray-800/60 p-3 rounded-lg border border-gray-700"
          >
            <span class="font-semibold text-lg text-white">
              {{ item.student_name }} — {{ item.course_name }}
            </span>
            <span class="text-sm text-gray-400">
              Email: {{ item.email }} | Phone: {{ item.phone_number }}
            </span>
            <span class="text-xs text-gray-500">
              City: {{ item.city }}, {{ item.state }} • Gender: {{ item.gender }}
            </span>
            <span class="text-xs text-gray-500">
              Applied on: {{ new Date(item.application_date).toLocaleDateString() }}
            </span>
            <span
              class="text-xs"
              :class="{
                'text-amber-400': item.status === 'pending',
                'text-rose-400': item.status === 'rejected',
                'text-cyan-400': item.status === 'accepted'
              }"
            >
              Status: {{ item.status }}
            </span>
          </li>
        </ul>

        <button
          class="mt-6 px-6 py-2 bg-gray-800/80 border border-gray-600 text-white rounded-full shadow hover:scale-105 transition"
          @click="showModal = false"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

/* ────────── Props ────────── */
const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'applications')

/* ────────── Types ────────── */
type Status = 'pending' | 'accepted' | 'rejected'

interface AnalyticsRow {
  id: number
  status: Status
  application_date: string
  student_name: string
  city: string
  gender: 'Male' | 'Female'
  course_name: string
  score: number | null
}

interface ApplicationDetail {
  application_id: number
  application_date: string
  status: Status
  student_id: number
  student_name: string
  email: string
  phone_number: number
  city: string
  state: string
  gender: 'Male' | 'Female'
  course_name: string
  school_name: string
}

/* ────────── State ────────── */
const analytics      = ref<AnalyticsRow[]>([])
const pendingCount   = computed(() => analytics.value.filter(a => a.status === 'pending').length)
const rejectedCount  = computed(() => analytics.value.filter(a => a.status === 'rejected').length)

const flippedCard    = ref<number>(-1)

const showModal      = ref(false)
const modalType      = ref<'pending' | 'rejected' | 'all'>('pending')
const modalData      = ref<ApplicationDetail[]>([])
const isLoadingModal = ref(false)

const API_BASE = 'http://localhost:8000'

/* ────────── Methods ────────── */
function flipCard(index: number) {
  flippedCard.value = index
}

async function openModal(type: 'pending' | 'rejected' | 'all') {
  modalType.value   = type
  showModal.value   = true
  isLoadingModal.value = true

  try {
    if (type === 'all') {
      // Fetch all 3 statuses concurrently and merge
      const [pending, accepted, rejected] = await Promise.all([
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/pending`),
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/accepted`),
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/rejected`)
      ])
      modalData.value = [...pending.data, ...accepted.data, ...rejected.data]
    } else {
      const { data } = await axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/${type}`)
      modalData.value = data
    }
  } catch (err) {
    console.error('Failed to fetch details', err)
    modalData.value = []
  } finally {
    isLoadingModal.value = false
  }
}

/* ────────── Fetch analytics on mount ────────── */
onMounted(async () => {
  try {
    const { data } = await axios.get<AnalyticsRow[]>(`${API_BASE}/analytics`)
    analytics.value = data
  } catch (err) {
    console.error('Could not fetch analytics data.', err)
  }
})
</script>

<style scoped>
/* ────────── BACKGROUND ────────── */
.futuristic-bg {
  background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
}

/* ────────── GLASS CARD ────────── */
.glassmorphic-card {
  background: linear-gradient(135deg, rgba(31, 41, 55, 0.9), rgba(17, 24, 39, 0.95));
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
  border-radius: 30px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(8px);
  width: 100%;
  height: 100%;
  padding: 2.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 0;
  left: 0;
  backface-visibility: hidden;
}

.border-cyan-400 { border-color: #22d3ee; }
.border-amber-400 { border-color: #fbbf24; }
.border-rose-400 { border-color: #fb7185; }

/* ────────── FLIP LOGIC ────────── */
.perspective-1000 { perspective: 1000px; }
.flip-card {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.7s cubic-bezier(.4,2.3,.3,1);
}
.flip-card-front { z-index: 2; }
.flip-card-back  { transform: rotateY(180deg); z-index: 1; }
.flip-card.flipped { transform: rotateY(180deg); }
</style>
