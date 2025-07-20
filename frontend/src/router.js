import { createRouter, createWebHistory } from 'vue-router'
import { usersStore } from '@/stores/user'
import { sessionStore } from '@/stores/session'
import { guardianStore } from '@/stores/my_students'

const routes = [
  { path: '/', redirect: '/my-students' },
  {
    path: '/my-students',
    name: 'My Students',
    component: () => import('@/pages/MyStudents.vue'),
  },
  {
    path: '/student/:student_name',
    name: 'Student Detail',
    component: () => import('@/pages/Student.vue'),
    props: true,
  },
  // {
  //   path: '/schedule',
  //   name: 'Schedule',
  //   component: () => import('@/pages/Schedule.vue'),
  // },
  // {
  //   path: '/grades',
  //   name: 'Grades',
  //   component: () => import('@/pages/Grades.vue'),
  // },
  {
    path: '/fees',
    name: 'Total Fees',
    component: () => import('@/pages/Fees.vue'),
  },
  // {
  //   path: '/attendance',
  //   name: 'Attendance',
  //   component: () => import('@/pages/Attendance.vue'),
  // },
  {
    path: '/:catchAll(.*)',
    redirect: '/schedule',
  },
]

let router = createRouter({
  history: createWebHistory('/parent-portal'),
  routes,
})

router.beforeEach(async (to, from) => {
  const { isLoggedIn, user: sessionUser } = sessionStore()
  const { user } = usersStore()
  const { guardian } = guardianStore()

  if (!isLoggedIn) {
    window.location.href = '/login'
    return await next(false)
  }

  if (user.data.length === 0) {
    await user.reload()
  }
  await guardian.reload()
})

export default router
