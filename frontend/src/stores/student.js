import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createResource } from 'frappe-ui'

export const studentStore = defineStore('zana-education-student', () => {
  const studentId = ref({})
  const studentInfo = ref({})
  const studentGroups = ref([])
  const studentSchedule = ref([])
  const studentEnrolledCourses = ref([])

  const student = createResource({
    url: 'zana_education.zana_education.api.get_zana_student_info',
    method: 'GET',
    params: () => ({ student_name: studentId.value }),
    auto: false,
    onSuccess(info) {
      if (!info) {
        window.location.href = '/app'
      }
      // remove current_program from info
      delete info.current_program
      studentInfo.value = info
    },
    onError(err) {
      console.error(err)
    },
  })

  const studentScheduleResource = createResource({
    url: 'zana_education.zana_education.api.get_course_schedule_for_zana_student',
    method: 'GET',
    params: () => ({ student_name: studentId.value }),
    auto: false,
    onSuccess: (response) => {
      let schedule = []
      response.forEach((classSchedule) => {
        schedule.push({
          title: classSchedule.title,
          with: classSchedule.instructor,
          name: classSchedule.name,
          room: classSchedule.room,
          date: classSchedule.schedule_date,
          from_time: classSchedule.from_time.split('.')[0],
          to_time: classSchedule.to_time.split('.')[0],
          color: classSchedule.class_schedule_color,
        })
      })
      studentSchedule.value = schedule
    },
  })

  const studentEnrolledCoursesResourse = createResource({
    url: 'zana_education.zana_education.api.get_enrolled_courses_for_student',
    method: 'GET',
    params: () => ({ student_name: studentId.value }),
    auto: false,
    onSuccess: (response) => {
      studentEnrolledCourses.value = response
    },
  })


  function loadStudent(student_name) {
    studentId.value = student_name
    student.reload({ student_name : student_name } )
    studentScheduleResource.reload({ student_name : student_name })
    studentEnrolledCoursesResourse.reload({ student_name : student_name })
  }

  function getStudentInfo() {
    return studentInfo
  }


  return {
    student,
    studentScheduleResource,
    studentEnrolledCourses,
    studentEnrolledCoursesResourse,
    studentSchedule,
    loadStudent,
    studentInfo,
    studentGroups,
    getStudentInfo,
  }
})
