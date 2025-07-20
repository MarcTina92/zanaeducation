<template>
  <div class="w-full h-full">
    <Calendar
      v-if="!store.studentScheduleResource.loading && store.studentScheduleResource.data"
      :events="store.studentSchedule"
    />
  </div>
</template>

<script setup>
  import Calendar from '@/components/Calendar.vue'
  import { studentStore } from '@/stores/student'
  const store = studentStore()
</script>
