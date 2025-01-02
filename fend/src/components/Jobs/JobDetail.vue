<template>
  <div class="container">
    <div class="job-detail">
      <h2 class="title">职位详情</h2>
      <div class="section">
        <h3>企业信息</h3>
        <div class="info">
          <p><span>企业名称：</span>{{ job.EnterpriseName }}</p>
          <p><span>企业类型：</span>{{ job.EnterpriseType }}</p>
          <p><span>邮箱：</span>{{ job.Email }}</p>
          <p><span>电话：</span>{{ job.Phone }}</p>
          <p><span>地址：</span>{{ job.Address }}</p>
          <p><span>邮政编码：</span>{{ job.PostalCode }}</p>
        </div>
      </div>
      <div class="section">
        <h3>职位信息</h3>
        <div class="info">
          <p><span>职位：</span>{{ job.Position }}</p>
          <p><span>招聘人数：</span>{{ job.Vacancies }}</p>
          <p><span>城市：</span>{{ job.City }}</p>
          <p><span>职位描述：</span>{{ job.Description }}</p>
          <p><span>发布时间：</span>{{ job.PublishTime }}</p>
          <p><span>点击量：</span>{{ job.Clicks }}</p>
          <p><span>薪资：</span>{{ job.Salary }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const baseURL = import.meta.env.VITE_APP_BASE_URL;
const route = useRoute()
const job = ref({})

const fetchJobDetails = async (jobId) => {
  try {
    const response = await axios.get(`${baseURL}/jobDetail/${jobId}`)
    job.value = response.data
  } catch (error) {
    console.error('Failed to fetch job details:', error)
    console.error('Error details:', error.response ? error.response.data : error.message)
  }
}

onMounted(() => {
  const jobId = route.params.job_id
  fetchJobDetails(jobId)
})
</script>

<style scoped>
/* 容器样式 */
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e0e7fa, #ffffff);
  padding: 20px;
}

/* 职位详情卡片 */
.job-detail {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-width: 800px;
  width: 100%;
  margin-top: -150px;
}

/* 标题样式 */
.title {
  background-color: #00bcd4;
  background-color:  #3f72af;
  color: #fff;
  padding: 20px;
  font-size: 28px;
  text-align: center;
  margin: 0;
}

/* 部分样式 */
.section {
  padding: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.section:last-child {
  border-bottom: none;
}

/* 信息样式 */
.info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px 20px;
  font-size: 16px;
  color: #555;
}

.info p {
  margin: 0;
}

.info span {
  font-weight: 600;
  color: #333;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .info {
    grid-template-columns: 1fr;
  }
}
</style>