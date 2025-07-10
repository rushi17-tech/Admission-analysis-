<!-- src/components/Schedule.vue -->
<script setup lang="ts">
import { ref, onMounted, computed, nextTick } from 'vue'
import axios from 'axios'
import FlipCard from '@/components/flipcard.vue'

interface ScheduleItem {
  title: string
  description: string
}

const props = defineProps<{ activeTab?: string }>()
const activeTab = computed(() => props.activeTab ?? 'schedule')

const BASE_URL  = 'http://localhost:8000/api'
const schedule  = ref<ScheduleItem[]>([])
const popoverIdx = ref<number|null>(null) // which card popover is open

const popoverPosition = ref<{top: number, left: number}|null>(null)
const selected = ref<ScheduleItem | null>(null)

function openDetails(item: ScheduleItem, idx: number, event: MouseEvent) {
  selected.value = item
  popoverIdx.value = idx
  // Position popover below the button
  const btn = (event.target as HTMLElement)
  const rect = btn.getBoundingClientRect()
  // Adjust for scrolling and a small vertical offset
  popoverPosition.value = {
    top: rect.bottom + window.scrollY + 8,
    left: rect.left + window.scrollX
  }
}

function closePopover() {
  popoverIdx.value = null
  selected.value = null
  popoverPosition.value = null
}

// Click outside handler
function onDocumentClick(e: MouseEvent) {
  const popover = document.getElementById('details-popover')
  if (popover && !popover.contains(e.target as Node)) {
    closePopover()
  }
}
onMounted(() => {
  document.addEventListener('click', onDocumentClick)
})
// Remove listener on unmount
import { onUnmounted } from 'vue'
onUnmounted(() => {
  document.removeEventListener('click', onDocumentClick)
})

onMounted(async () => {
  try {
    const { data } = await axios.get<ScheduleItem[]>(`${BASE_URL}/schedule`)
    schedule.value = data
  } catch (err) {
    console.error('Could not load schedule – demo fallback', err)
    schedule.value = [
      {
        title: 'Demo Entrance Exam – Round 1',
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
    class="relative py-10 px-3 md:px-10 min-h-[82vh] animate-fade-in text-white"
  >
    <!-- ───── title on blurred strip ───── -->
    <h3 class="page-heading mb-12 text-4xl font-extrabold tracking-wide text-center">
      Entrance&nbsp;Exam&nbsp;Schedule
    </h3>

    <!-- ───── schedule cards ───── -->
    <div class="schedule-grid max-w-7xl mx-auto">
      <FlipCard
        v-for="(item, idx) in schedule"
        :key="idx"
        class="schedule-card"
      >
        <!-- front -->
        <template #default>
          <div class="card-face">
            <h4 class="card-title">{{ item.title }}</h4>
            <button class="card-btn"
              @click.stop="openDetails(item, idx, $event)">
              Show&nbsp;Details
            </button>
            <!-- Popover for this card -->
            <transition name="fade">
              <div
                v-if="popoverIdx === idx && popoverPosition"
                :id="'details-popover'"
                class="popover-panel"
                :style="{
                  position: 'absolute',
                  top: popoverPosition.top + 'px',
                  left: popoverPosition.left + 'px'
                }"
                @click.stop
              >
                <div class="popover-content">
                  <h4 class="modal-title">{{ selected?.title }}</h4>
                  <p class="modal-desc" v-html="selected?.description" />
                  <button class="modal-btn" @click="closePopover">Close</button>
                </div>
              </div>
            </transition>
          </div>
        </template>

        <!-- back -->
        <template #back>
          <div class="card-face card-back">
            <p class="card-desc" v-html="item.description" />
            <button class="card-btn"
              @click.stop="openDetails(item, idx, $event)">
              Show&nbsp;Details
            </button>
            <!-- Popover for this card (back side) -->
            <transition name="fade">
              <div
                v-if="popoverIdx === idx && popoverPosition"
                :id="'details-popover'"
                class="popover-panel"
                :style="{
                  position: 'absolute',
                  top: popoverPosition.top + 'px',
                  left: popoverPosition.left + 'px'
                }"
                @click.stop
              >
                <div class="popover-content">
                  <h4 class="modal-title">{{ selected?.title }}</h4>
                  <p class="modal-desc" v-html="selected?.description" />
                  <button class="modal-btn" @click="closePopover">Close</button>
                </div>
              </div>
            </transition>
          </div>
        </template>
      </FlipCard>
    </div>
  </div>
</template>

<style scoped>
.page-heading {
  @apply inline-block px-6 py-3 rounded-2xl;
  background: rgba(17, 24, 39, 0.55);
  backdrop-filter: blur(14px) saturate(160%);
}
.schedule-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2.5rem;
  justify-items: center;
}
.schedule-card {
  width: 320px;
  height: 370px;
  border-radius: 1.5rem;
  border: 1.5px solid rgba(255, 255, 255, 0.1);
  background: rgba(17, 24, 39, 0.55);
  backdrop-filter: blur(18px) saturate(160%);
  box-shadow: 0 6px 32px rgba(74, 222, 255, 0.15),
              0 1.5px 8px rgba(139, 92, 246, 0.15);
  transition: transform 0.18s, box-shadow 0.2s, border-color 0.2s;
  position: relative;
}
.schedule-card:hover,
.schedule-card:focus-within {
  transform: translateY(-5px) scale(1.025);
  border-color: #6366f1;
  box-shadow:
    0 0 0 2.5px #3b82f6,
    0 6px 32px rgba(74, 222, 255, 0.18),
    0 1.5px 8px rgba(139, 92, 246, 0.19);
}
.card-face {
  @apply flex flex-col items-center justify-center h-full p-8 text-center;
  position: relative;
}
.card-back {
  background: rgba(31, 41, 55, 0.65);
  border: 1.5px solid #6366f1;
}
.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #60a5fa;
  margin-bottom: 1.2rem;
  text-shadow: 0 0 6px #3b82f6aa;
}
.card-desc {
  color: #c7d2fe;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  word-break: break-word;
}
.card-btn,
.modal-btn {
  @apply rounded-lg font-medium shadow text-white;
  background: linear-gradient(90deg, #6366f1 40%, #8b5cf6 100%);
  transition: background 0.18s, box-shadow 0.18s, transform 0.15s;
}
.card-btn {
  padding: 0.5rem 1.5rem;
}
.modal-btn {
  width: 100%;
  padding: 0.75rem 0;
}
.card-btn:hover,
.card-btn:focus,
.modal-btn:hover,
.modal-btn:focus {
  background: linear-gradient(90deg, #8b5cf6 20%, #6366f1 100%);
  box-shadow: 0 0 24px #8b5cf6cc;
  transform: scale(1.04);
}
/* Popover styles */
.popover-panel {
  z-index: 200;
  min-width: 320px;
  max-width: 340px;
  background: rgba(17, 24, 39, 0.98);
  border-radius: 1.25rem;
  box-shadow: 0 8px 32px rgba(74,222,255,0.18), 0 1.5px 8px rgba(139,92,246,0.19);
  border: 1.5px solid #6366f1;
  padding: 0;
  /* Remove pointer-events so click outside works */
}
.popover-content {
  @apply p-6 text-center;
}
.modal-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 1.2rem;
  text-shadow: 0 0 8px #8b5cf6;
}
.modal-desc {
  color: #d1d5db;
  margin-bottom: 2rem;
  font-size: 1.05rem;
  line-height: 1.6;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fadeIn 0.6s ease forwards; }
</style>
