<!-- src/components/Schedule.vue -->
<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import FlipCard from '@/components/flipcard.vue'

interface ScheduleItem {
  title: string
  description: string          // already formatted by the API (may contain <strong> tags)
}

const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'schedule')

// ────────── STATE ──────────
const BASE_URL = 'http://localhost:8000/api'
const schedule      = ref<ScheduleItem[]>([])   // cards loaded from backend
const showModal     = ref(false)                // controls modal visibility
const selectedItem  = ref<ScheduleItem | null>(null) // card user tapped

// ────────── METHODS ──────────
function openDetails(item: ScheduleItem) {
  selectedItem.value = item
  showModal.value = true
}

// ────────── LIFECYCLE ──────────
onMounted(async () => {
  try {
    const { data } = await axios.get<ScheduleItem[]>(`${BASE_URL}/schedule`)
    schedule.value = data
  } catch (err) {
    console.error('Could not load schedule; falling back to demo cards.', err)
    // optional fallback so the UI isn’t empty if backend is down
    schedule.value = [
      {
        title: 'Demo Entrance Exam – Round 1',
        description:
          'The entrance exam is scheduled for <strong>05 July</strong>. ' +
          'Report by <strong>09:00 AM</strong>. Round <strong>1</strong>.'
      }
    ]
  }
})
</script>

<template>
  <div
    v-if="activeTab === 'schedule'"
    class="p-8 min-h-screen bg-[#12131c] space-y-10 transition-colors duration-500"
  >
    <!-- ────────── PAGE TITLE ────────── -->
    <h3 class="text-4xl font-extrabold text-white mb-8 tracking-wide text-center font-sans">
      Entrance Exam Schedule
    </h3>

    <!-- ────────── CARD GRID ────────── -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10 max-w-7xl mx-auto">
      <FlipCard
        v-for="(item, idx) in schedule"
        :key="idx"
        class="mx-auto w-[320px] h-[350px]"
      >
        <!-- ────────── CARD FRONT ────────── -->
        <template #default>
          <div
            class="flex flex-col items-center justify-center h-full bg-[#1e202f] rounded-2xl border border-[#2f3245] p-6 transition-colors duration-300 hover:border-blue-500"
          >
            <h4 class="text-xl font-semibold text-blue-400 mb-3 text-center">
              {{ item.title }}
            </h4>

            <!-- Show Details button -->
            <button
              @click.stop="openDetails(item)"
              class="mt-4 px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              Show&nbsp;Details
            </button>
          </div>
        </template>

        <!-- ────────── CARD BACK ────────── -->
        <template #back>
          <div
            class="flex flex-col items-center justify-center h-full bg-[#23253f] rounded-2xl border border-blue-600 p-6 text-center"
          >
            <p
              class="text-blue-200 text-sm leading-relaxed"
              v-html="item.description"
            />
            <button
              @click.stop="openDetails(item)"
              class="mt-4 px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              Show&nbsp;Details
            </button>
          </div>
        </template>
      </FlipCard>
    </div>

    <!-- ────────── DETAILS MODAL ────────── -->
    <div
      v-if="showModal"
      @click.self="showModal = false"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
    >
      <div class="bg-[#1e202f] w-full max-w-md rounded-2xl p-6 shadow-lg">
        <h4 class="text-2xl font-semibold text-white mb-4">
          {{ selectedItem?.title }}
        </h4>

        <p
          class="text-gray-300 leading-relaxed mb-6"
          v-html="selectedItem?.description"
        />

        <button
          @click="showModal = false"
          class="w-full px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
        >
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* optional subtle glow on hover for the button / numbers */
.drop-shadow-glow {
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
}
</style>
