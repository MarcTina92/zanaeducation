<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { studentStore } from '@/stores/student'

// Tab Components (replace with real ones)
import ScheduleTab from '@/components/student/ScheduleTab.vue'
import CoursesTab from '@/components/student/CoursesTab.vue'
// import PaymentDueTab from '@/components/student/PaymentDueTab.vue'
// import InvoicesTab from '@/components/student/InvoicesTab.vue'
// import AttendanceTab from '@/components/student/AttendanceTab.vue'

const route = useRoute()
const store = studentStore()
const tabs = ['Schedule', 'Courses', 'Payment Due', 'Invoices', 'Attendance']
const activeTab = ref(route.query.tab || 'Schedule')
// Update URL when tab changes
function setActiveTab(tab) {
  activeTab.value = tab
}
store.loadStudent(route.params.student_name)
</script>

<template>
  <div class="p-6">
    <div v-if="store.studentInfo">
      <h1 class="text-2xl font-bold">{{ store.studentInfo.customer }}</h1>
      <div class="p-6">
      <!-- Tabs -->
      <div class="flex space-x-4 border-b mb-4">
        <button
          v-for="t in tabs"
          :key="t"
          @click="setActiveTab(t)"
          class="py-2 px-4 border-b-2"
          :class="{
            'border-blue-600 text-blue-600 font-semibold': activeTab === t,
            'border-transparent text-gray-600 hover:text-black': activeTab !== t
          }"
        >
          {{ t }}
        </button> 
    </div>

      <!-- Tab Content -->
      <div v-if="activeTab === 'Schedule'">
        <ScheduleTab/>
      </div>
      <div v-else-if="activeTab === 'Courses'">
        <CoursesTab/>
      </div>
      <div v-else-if="activeTab === 'Payment Due'">
        <PaymentDueTab :student="studentInfo" />
      </div>
      <div v-else-if="activeTab === 'Invoices'">
        <InvoicesTab :student="studentInfo" />
      </div>
      <div v-else-if="activeTab === 'Attendance'">
        <AttendanceTab :student="studentInfo" />
      </div>
    </div>
    </div>
  </div>
  
</template>
