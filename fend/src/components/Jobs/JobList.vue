<template>
  <div class="context">
    <div class="job-list">
      <div class="search-section">
        <input v-model="searchParams.keyword" class="search-input" placeholder="输入职位或企业名称" />
        <input v-model="searchParams.location" class="search-input" placeholder="输入工作地点" />
        <button @click="handleSearch" class="search-button">搜索</button>
      </div>
      <div class="job-listings">
        <div v-for="job in filteredJobs" :key="job.EnterpriseID" class="job-card">
          <div class="job-header">
            <h3>{{ job.Position }} [{{ job.City }}]</h3>
            <p style="color:#112d4e; font-weight: bold;">{{ job.EnterpriseType }} · {{ job.EnterpriseName }}</p>
          </div>
          <div class="job-details">
            <p style="color: #FE5767 ; font-size: 20px; font-weight: bold;">{{ job.Salary }}</p>
            <p style="color: #AAAAAA; font-weight: bold;">{{ job.Clicks }}Clicks</p>
          </div>
          <div class="job-actions">
            <router-link :to="`/jobDetail/${job.JobID}`" @click.native="incrementClicks(job.JobID)">
              <button class="details-button" style="font-weight: bold;">查看详情</button>
            </router-link>
            <router-link :to="`/apply/${job.JobID}`">
              <button class="apply-button" style="font-weight: bold;">申请职位</button>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const baseURL = import.meta.env.VITE_APP_BASE_URL;
const jobs = ref([])
const searchParams = ref({
  keyword: '',
  location: '',
  jobType: ''
})

const fetchJobs = async () => {
  try {
    const response = await axios.get(`${baseURL}/jobList/`)
    jobs.value = response.data.jobList
  } catch (error) {
    console.error('Failed to fetch jobs:', error)
    console.error('Error details:', error.response ? error.response.data : error.message)
  }
}

const handleSearch = () => {
  fetchJobs()
}

const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    return (
      (job.Position.toLowerCase().includes(searchParams.value.keyword.toLowerCase()) ||
      job.EnterpriseName.toLowerCase().includes(searchParams.value.keyword.toLowerCase())) &&
      job.City.toLowerCase().includes(searchParams.value.location.toLowerCase())
    )
  })
})

const incrementClicks = async (jobID) => {
  try {
    await axios.post(`${baseURL}/incrementClicks/${jobID}`)
    fetchJobs() // 更新job列表以反映点击次数的变化
  } catch (error) {
    console.error('Failed to increment clicks:', error)
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.context {
  background: linear-gradient(to bottom, rgba(116, 185, 255, 0.5), rgba(255, 255, 255, 0.8)); /* 修改整体背景颜色并加上透明度 */
  /* background: linear-gradient(135deg, #e0e7fa, #ffffff); */
  
  background-attachment: fixed; /* 固定背景渐变 */
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}


.job-list {
  font-family: Arial, sans-serif;
  color: #333;
  margin: 20px auto;
  width: 900px;
  margin-top: 100px;
  /* background: linear-gradient(to bottom, #74b9ff, #0984e3);
  padding: 20px;
  border-radius: 10px; */
}

.search-section {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  margin-right: 10px;
  padding: 10px;
  border: 2px solid #007bff;
  border-radius: 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}

.job-card {
  display: flex;
  flex-direction: column;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 15px;
  background-color: white;
  transition: box-shadow 0.3s ease;
}

.job-card:hover {
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid rgba(0, 123, 255, 0.8);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: px;
}

.job-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #007bff;
}

/* .job-header p {
  margin: 0;
  font-size: 0.9em;
  color: #555;
} */

.job-details {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.job-details p {
  margin: 0;
  font-size: 0.9em;
  color: #333;
}

.job-actions {
  display: flex;
  justify-content: space-between;
}

.details-button {
  padding: 10px 20px;
  background-color: #3f72af;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.details-button:hover {
  background-color: #3f72af;
}

.apply-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.apply-button:hover {
  background-color: #0056b3;
}
</style>
