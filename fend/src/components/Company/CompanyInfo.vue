<template>
  <div class="container">
    <div class="company-info">
      <h2 class="title">企业信息维护</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>企业名称：</label>
          <input type="text" v-model="company.EnterpriseName" required />
        </div>
        <div class="form-group">
          <label>企业地址：</label>
          <input type="text" v-model="company.Address" required />
        </div>
        <div class="form-group">
          <label>联系邮箱：</label>
          <input type="email" v-model="company.Email" required />
        </div>
        <button type="submit" class="submit-button">保存信息</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const baseURL = import.meta.env.VITE_APP_BASE_URL;
const company = ref({
  EnterpriseName: '',
  Address: '',
  Email: ''
})

const fetchCompanyInfo = async (username) => {
  try {
    const response = await axios.get(`${baseURL}/enterpriseInfo/${username}`)
    company.value = response.data
  } catch (error) {
    console.error('获取企业信息失败', error)
  }
}

const handleSubmit = async () => {
  try {
    const token = localStorage.getItem('token')
    const userResponse = await axios.get(`${baseURL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const username = userResponse.data.username
    await axios.put(`${baseURL}/enterpriseInfoUpdate/${username}`, {
      enterprisename: company.value.EnterpriseName,
      address: company.value.Address,
      email: company.value.Email
    }, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    alert('企业信息已保存！')
  } catch (error) {
    console.error('保存企业信息失败', error)
    alert('保存企业信息失败')
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    const userResponse = await axios.get(`${baseURL}/users/me`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const username = userResponse.data.username
    await fetchCompanyInfo(username)
  } catch (error) {
    console.error('获取用户信息失败', error)
  }
})
</script>

<style scoped>
/* 容器样式 */
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));

  padding: 20px;
}

/* 企业信息卡片 */
.company-info {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  max-width: 600px;
  width: 100%;
  padding: 20px;
}

/* 标题样式 */
.title {
  background-color: rgba(0, 180, 179, 1);
  
  color: #fff;
  padding: 20px;
  font-size: 28px;
  text-align: center;
  margin: -20px -20px 20px -20px;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

/* 提交按钮样式 */
.submit-button {
  background-color: #00bcd4;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0097a7;
}
</style>