<!-- ScheduleTab.vue -->
<template>
  <div>
    <h2 class="text-xl font-bold">Schedule</h2>
    <p v-if="!student">No student data</p>
    <pre v-else>{{ student }}</pre>
  </div>
</template>

<script setup>
defineProps(['student'])
</script>
