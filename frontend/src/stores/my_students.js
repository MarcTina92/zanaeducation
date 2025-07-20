import { defineStore } from 'pinia'
import { ref } from 'vue'
import { createResource } from 'frappe-ui'

export const guardianStore = defineStore('zana-education-guardian', () => {
  const guardianInfo  = ref({})
  
  const guardian = createResource({
    url: 'zana_education.zana_education.api.get_guardian_info',
    onSuccess(info) {
      if (!info) {
        window.location.href = '/app'
      }
      guardianInfo.value = info
    },
    onError(err) {
      console.error(err)
    },
  })

  function getGuardianInfo() {
    return guardianInfo
  }

  return {
    guardian,
    guardianInfo,
    getGuardianInfo,
  }
})
