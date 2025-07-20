<template>
  <div class="p-4 space-y-6">
    <div class="grid">
      <h3 class="text-xl font-semibold mb-1">My Students</h3>
    </div>

    <!-- Student Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <Card
        v-for="student in students"
        :key="student.name"
        class="p-6 flex flex-col items-center text-center bg-white rounded-xl shadow hover:shadow-lg transition"
      >
        <!-- Centered image/logo -->
        <div class="w-24 h-24 mb-4" style="margin: auto">
          <img
            :src="student.image"
            alt="Student Image"
            class="w-full h-full object-cover rounded-full mx-auto"
          />
        </div>
        <h3 class="text-xl font-semibold mb-1">{{ student.student_name }}</h3>
        <p class="text-gray-600 mb-1">{{ student.email }}</p>
        <p class="text-gray-500 text-sm mb-2">
          <strong>Birth Date:</strong> {{ student.birth_date }}
        </p>
        <Button @click="viewStudent(student)">View</Button>
      </Card>
    </div>

  </div>
</template>
<script setup>
import { ref } from 'vue'
import { guardianStore } from '@/stores/my_students'
import { useRouter } from 'vue-router'
const { getGuardianInfo , getGuardianStudentInfo } = guardianStore()
const router = useRouter()
const guardianInfo = ref(getGuardianInfo()?.value?.guardian)
const students = ref(getGuardianInfo()?.value?.students)

// Add your viewStudent method here
function viewStudent(student) {
  // Navigate to student details page, or show a modal, or set a selectedStudent ref
  // Example if routing:

  router.push(`/student/${student.name}`)
}

</script>

<style></style>
