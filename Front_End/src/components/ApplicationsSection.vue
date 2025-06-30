<template>
  <!-- Applications tab -->
  <div
    v-if="activeTab === 'applications'"
    class="relative py-10 px-3 md:px-10 min-h-[82vh] animate-fade-in text-white"
  >
    <!-- ────────── PAGE TITLE ────────── -->
    <h3 class="mb-12 text-4xl font-extrabold tracking-wide flex items-center gap-3">
      <span
        class="inline-flex items-center gap-3 bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent"
      >
        <svg class="w-10 h-10" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M12 4v16m8-8H4" />
        </svg>
        Applications&nbsp;Overview
      </span>
    </h3>

    <!-- ────────── FLIP‑CARDS GRID ────────── -->
    <div class="grid gap-10 grid-cols-[repeat(auto-fit,minmax(260px,1fr))]">
      <!-- CARD 0 — NEW APPLICATIONS -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card">
          <div class="flip-card-front glass-card border border-cyan-400/40">
            <svg class="w-12 h-12 text-cyan-400 mb-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M16 21v-2a4 4 0 0 0-3-3.87M6 21v-2a4 4 0 0 1 3-3.87m6-7a4 4 0 1 1-8 0 4 4 0 0 1 8 0Zm6 4v6m3-3h-6" />
            </svg>
            <h4 class="text-2xl font-bold mb-2">New Applications</h4>
            <span class="text-6xl font-extrabold text-cyan-300 mb-4 animate-pulse">{{ analytics.length }}</span>
            <button class="action-btn" @click="openModal('all')">Show Details</button>
          </div>
        </div>
      </div>

      <!-- CARD 1 — DOCUMENTS PENDING -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card" :class="{ flipped: flippedCard === 1 }">
          <!-- FRONT -->
          <div class="flip-card-front glass-card border border-amber-400/40">
            <svg class="w-12 h-12 text-amber-400 mb-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path d="M7 7h10M7 11h10M7 15h6M5 19h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2Z" />
            </svg>
            <h4 class="text-2xl font-bold mb-2">Documents Pending</h4>
            <span class="text-6xl font-extrabold text-amber-300 mb-4 animate-pulse">{{ pendingCount }}</span>
            <button class="action-btn" @click="flipCard(1)">Show Details</button>
          </div>

          <!-- BACK -->
          <div class="flip-card-back glass-card border border-amber-400/40">
            <h4 class="text-xl font-semibold mb-2">Details</h4>
            <ul class="text-base text-gray-200 text-center space-y-1 mb-4">
              <li><b>{{ pendingCount }}</b> applications require additional documentation.</li>
              <li v-if="pendingCount === 0">Great news — nothing is pending!</li>
              <li v-else>Click below for the full list.</li>
            </ul>
            <button class="mini-btn mb-3" @click="openModal('pending')">View More</button>
            <button class="action-btn" @click="flipCard(-1)">Back</button>
          </div>
        </div>
      </div>

      <!-- CARD 2 — REJECTED -->
      <div class="relative perspective-1000 mx-auto" style="width:340px;height:400px;">
        <div class="flip-card" :class="{ flipped: flippedCard === 2 }">
          <!-- FRONT -->
          <div class="flip-card-front glass-card border border-rose-400/40">
            <svg class="w-12 h-12 text-rose-400 mb-3" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" /><line x1="4" y1="4" x2="20" y2="20" />
            </svg>
            <h4 class="text-2xl font-bold mb-2">Rejected Applications</h4>
            <span class="text-6xl font-extrabold text-rose-300 mb-4 animate-pulse">{{ rejectedCount }}</span>
            <button class="action-btn" @click="flipCard(2)">Show Details</button>
          </div>

          <!-- BACK -->
          <div class="flip-card-back glass-card border border-rose-400/40">
            <h4 class="text-xl font-semibold mb-2">Details</h4>
            <ul class="text-base text-gray-200 text-center space-y-1 mb-4">
              <li><b>{{ rejectedCount }}</b> applications have been rejected.</li>
              <li v-if="rejectedCount === 0">No rejections 🎉</li>
              <li v-else>Click below for the full list.</li>
            </ul>
            <button class="mini-btn mb-3" @click="openModal('rejected')">View More</button>
            <button class="action-btn" @click="flipCard(-1)">Back</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ────────── MODAL ────────── -->
    <transition name="fade">
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-window border-gray-300/20">
          <h4 class="modal-title">
            {{
              modalType === 'all'
                ? 'All Applications'
                : modalType === 'pending'
                ? 'Pending Applications'
                : 'Rejected Applications'
            }}
          </h4>

          <!-- Loading -->
          <p v-if="isLoadingModal" class="text-center text-gray-200">Loading…</p>
          <ul v-else class="space-y-3 h-96 overflow-y-auto pr-2">
            <li
              v-for="item in modalData"
              :key="item.application_id"
              class="flex flex-col glass-list-item"
            >
              <span class="font-semibold text-lg">{{ item.student_name }} — {{ item.course_name }}</span>
              <span class="text-sm text-gray-300">
                Email: {{ item.email }} • Phone: {{ item.phone_number }}
              </span>
              <span class="text-xs text-gray-400">
                {{ item.city }}, {{ item.state }} • Gender: {{ item.gender }}
              </span>
              <span class="text-xs text-gray-400">
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

          <button class="action-btn mt-8 w-full" @click="showModal = false">Close</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
/* ────────── imports & logic (UNCHANGED) ────────── */
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'applications')

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

const analytics      = ref<AnalyticsRow[]>([])
const pendingCount   = computed(() => analytics.value.filter(a => a.status === 'pending').length)
const rejectedCount  = computed(() => analytics.value.filter(a => a.status === 'rejected').length)

const flippedCard    = ref<number>(-1)
const showModal      = ref(false)
const modalType      = ref<'pending' | 'rejected' | 'all'>('pending')
const modalData      = ref<ApplicationDetail[]>([])
const isLoadingModal = ref(false)
const API_BASE       = 'http://localhost:8000'

function flipCard(i:number){ flippedCard.value = i }
async function openModal(t:'pending'|'rejected'|'all'){
  modalType.value = t
  showModal.value = true
  isLoadingModal.value = true
  try{
    if(t==='all'){
      const [p,a,r] = await Promise.all([
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/pending`),
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/accepted`),
        axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/rejected`)
      ])
      modalData.value = [...p.data, ...a.data, ...r.data]
    }else{
      const { data } = await axios.get<ApplicationDetail[]>(`${API_BASE}/applications/status/${t}`)
      modalData.value = data
    }
  }catch(e){
    console.error('fetch failed', e)
    modalData.value = []
  }finally{
    isLoadingModal.value = false
  }
}
onMounted(async()=>{
  try{
    const { data } = await axios.get<AnalyticsRow[]>(`${API_BASE}/analytics`)
    analytics.value = data
  }catch(e){ console.error('analytics fetch failed', e) }
})
</script>

<style scoped>
/* ────────── glass utilities ────────── */
.glass-card{
  @apply flex flex-col items-center justify-center p-9 rounded-3xl
          border border-white/10 shadow-xl transition-all duration-300 hover:scale-105;
  background: rgba(17,24,39,0.55);        /* deep slate */
  backdrop-filter: blur(18px) saturate(160%);
}
.action-btn{
  @apply mt-4 px-6 py-2 rounded-full shadow text-white
          bg-gray-800/70 border border-gray-600 hover:scale-105 transition;
}
.mini-btn{
  @apply px-5 py-1 rounded-full shadow text-white
          bg-gray-800/70 border border-gray-600 hover:scale-105 transition;
}

/* ────────── flip‑card mechanics (unchanged) ────────── */
.perspective-1000{ perspective:1000px; }
.flip-card{ @apply w-full h-full relative; transform-style:preserve-3d; transition:transform .7s cubic-bezier(.4,2.3,.3,1); }
.flip-card-front{ z-index:2; backface-visibility:hidden; }
.flip-card-back { transform:rotateY(180deg); backface-visibility:hidden; }
.flip-card.flipped{ transform:rotateY(180deg); }

/* ────────── modal glass ────────── */
.modal-backdrop{ @apply fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-lg; }
.modal-window{
  @apply rounded-2xl shadow-2xl w-full max-w-xl p-8 border flex flex-col text-white;
  background: rgba(17,24,39,0.65);
  backdrop-filter: blur(22px) saturate(160%);
}
.modal-title{ @apply text-2xl font-bold mb-4; }
.glass-list-item{
  @apply rounded-lg border border-white/10 p-3;
  background: rgba(31,41,55,0.5);
  backdrop-filter: blur(15px) saturate(150%);
}

/* ────────── fade & entry animation ────────── */
.fade-enter-active,.fade-leave-active{ transition:opacity .3s; }
.fade-enter-from,.fade-leave-to{ opacity:0; }
@keyframes fadeIn{ from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.animate-fade-in{ animation:fadeIn .6s ease forwards; }
</style>
