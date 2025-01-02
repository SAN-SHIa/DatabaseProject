<template>
  <div class="container">
    <div class="job-detail">
      <h2 class="title">职位申请</h2>
      <div v-if="job" class="section">
        <h3>职位信息</h3>
        <div class="info">
          <p><span>企业名称：</span>{{ job.EnterpriseName }}</p>
          <p><span>企业类型：</span>{{ job.EnterpriseType }}</p>
          <p><span>城市：</span>{{ job.City }}</p>
          <p><span>地址：</span>{{ job.Address }}</p>
          <p><span>职位：</span>{{ job.Position }}</p>
          <p><span>薪资：</span>{{ job.Salary }}</p>
        </div>
      </div>
      <div v-if="resume" class="section">
        <h3>我的简历</h3>
        <div class="info">
          <p><span>姓名：</span>{{ resume.Username }}</p>
          <p><span>性别：</span>{{ resume.Gender }}</p>
          <p><span>邮箱：</span>{{ resume.Email }}</p>
          <p><span>电话：</span>{{ resume.Phone }}</p>
          <p><span>地址：</span>{{ resume.Address }}</p>
          <p><span>教育背景：</span>{{ resume.Education }}</p>
          <p><span>技能：</span>{{ resume.Skills }}</p>
          <p><span>期望职位：</span>{{ resume.Position }}</p>
          <p><span>期望城市：</span>{{ resume.City }}</p>
          <p><span>期望薪资：</span>{{ resume.Salary }}</p>
          <p><span>自我介绍：</span>{{ resume.Introduction }}</p>
        </div>
      </div>
      <form @submit.prevent="handleSubmit" class="section" >
        <button type="submit">提交申请</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const baseURL = import.meta.env.VITE_APP_BASE_URL;
const route = useRoute()
const router = useRouter()
const job = ref(null)
const resume = ref(null)
const application = ref({
  UserID: '',
  EnterpriseID: '',
  Name: '',
  EnterpriseName: '',
  HiringDepartment: '',
  Position: '',
  ApplicationDate: new Date().toISOString()
})

onMounted(async () => {
  try {
    // 获取职位详情
    const jobResponse = await axios.get(`${baseURL}/apply/${route.params.jobId}`)
    job.value = jobResponse.data

    // 获取用户简历
    const resumeResponse = await axios.get(`${baseURL}/getResume/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    
    if (!resumeResponse.data.resume) {
      alert('请先完成简历')
      router.push('/resume')
      return
    }

    resume.value = resumeResponse.data.resume

    application.value.UserID = resume.value.UserID;
    application.value.EnterpriseID = job.value.EnterpriseID;
    application.value.Name = resume.value.Username;
    application.value.EnterpriseName = job.value.EnterpriseName;
    application.value.HiringDepartment = job.value.HiringDepartment;
    application.value.Position = job.value.Position;
  } catch (error) {
    console.error('Failed to fetch data:', error)
  }
})

const handleSubmit = async () => {
  try {
    const response = await axios.post(`${baseURL}/submitApply/`, application.value, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    alert('申请提交成功！')
    router.push('/jobs')
  } catch (error) {
    console.error('Failed to submit application:', error)
    console.log(application.value)
  }
}
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
  margin-top: 50px;
}

/* 标题样式 */
.title {
  background-color: #3f72af;
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

/* 提交按钮样式 */
button[type="submit"] {
  background-color: #00bcd4;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  display: block;
  margin: 0 auto;
}

button[type="submit"]:hover {
  background-color: #0097a7;
}

/* 响应式设计 */
@media (max-width: 600px) {
  .info {
    grid-template-columns: 1fr;
  }
}
</style>