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
            <router-link :to="`/jobDetail/${job.JobID}`">
              <button class="details-button" style="font-weight: bold;">查看详情</button>
            </router-link>
            <button @click="deleteJob(job.JobID)" class="delete-button" style="font-weight: bold;">删除职位</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const jobs = ref([])
const searchParams = ref({
  keyword: '',
  location: '',
  jobType: ''
})

const baseURL = import.meta.env.VITE_APP_BASE_URL

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

const deleteJob = async (jobID) => {
  try {
    await axios.delete(`${baseURL}/manageJob/${jobID}`)
    fetchJobs() // 重新获取职位列表
  } catch (error) {
    console.error('Failed to delete job:', error)
    console.error('Error details:', error.response ? error.response.data : error.message)
  }
}

onMounted(() => {
  fetchJobs()
})
</script>

<style scoped>
.context {
  background: linear-gradient(to bottom, rgba(255, 126, 95, 0.1), rgba(254, 180, 123, 0.5));
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
  border: 2px solid #ff8c00;
  border-radius: 4px;
}

.search-button {
  padding: 10px 20px;
  background-color: #ff8c00;
  color: white;
  border: 2px solid #e07b00;
  border-radius: 4px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #e07b00;
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
  border: 2px solid rgba(255, 140, 0, 0.8);
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
  color: #ff8c00;
}

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
  background-color: #ff8c00;
  color: white;
  border: 2px solid #e07b00;
  border-radius: 4px;
  cursor: pointer;
}

.details-button:hover {
  background-color: #e07b00;
}

.apply-button {
  padding: 10px 20px;
  background-color: #ff8c00;
  color: white;
  border: 2px solid #e07b00;
  border-radius: 4px;
  cursor: pointer;
}

.apply-button:hover {
  background-color: #e07b00;
}

.delete-button {
  padding: 10px 20px;
  background-color: #ff4d4f;
  color: white;
  border: 2px solid #d9363e;
  border-radius: 4px;
  cursor: pointer;
}

.delete-button:hover {
  background-color: #d9363e;
}
</style>
