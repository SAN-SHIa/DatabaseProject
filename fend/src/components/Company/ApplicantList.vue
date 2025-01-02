<template>
  <div class="applicant-list">
    <h2>应聘人员信息查询</h2>
    <ul>
      <li v-for="applicant in applicants" :key="applicant.id">
        {{ applicant.name }} - {{ applicant.position }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const applicants = ref([
  { id: 1, name: '张三', position: '前端开发' },
  { id: 2, name: '李四', position: '后端开发' }
])

// 这里可以添加获取应聘人员信息的逻辑
</script>

<style scoped>
.applicant-list {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
</style>