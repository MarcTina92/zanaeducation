<!-- ScheduleTab.vue -->
<template>
  <div class="row">
    <div class="col-md-6">
      <div class="card mb-4 shadow-sm">
        <div class="card-body">
            <div v-for="(item, index) in store.studentEnrolledCourses" :key="index">
              {{ item.course }}
            </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { studentStore } from '@/stores/student'
  const store = studentStore()
</script>
