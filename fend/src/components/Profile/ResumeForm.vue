<template>
  <div class = "context">
  <div class="resume-form">
    <h2>个人简历</h2>
    <form @submit.prevent="handleSubmit">
      <section>
        <h3>基本信息</h3>
        <div class="form-row">
          <div class="form-group">
            <label>用户名：</label>
            <input type="text" v-model="formData.Username" required disabled />
          </div>
          <div class="form-group">
            <label>性别：</label>
            <input type="text" v-model="formData.Gender" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>邮箱：</label>
            <input type="email" v-model="formData.Email" required />
          </div>
          <div class="form-group">
            <label>电话：</label>
            <input type="text" v-model="formData.Phone" />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>地址：</label>
            <input type="text" v-model="formData.Address" />
          </div>
          <div class="form-group">
            <label>邮政编码：</label>
            <input type="text" v-model="formData.PostalCode" />
          </div>
        </div>

      </section>

      <section>
        <h3>教育背景</h3>
        <div class="form-row">
          <div class="form-group">
            <label>教育：</label>
              <input type="text" v-model="formData.Education" />
            </div>
          <div class="form-group">
            <label>技能：</label>
            <!-- <textarea v-model="formData.Skills"></textarea> -->
            <input type="text" v-model="formData.Skills" />
          </div>
        </div>
      </section>

      <section>
        <h3>工作意向</h3>
        <div class="form-row">
          <div class="form-group">
            <label>工作类型：</label>
            <input type="text" v-model="formData.JobType" />
          </div>
          <div class="form-group">
            <label>职位：</label>
            <input type="text" v-model="formData.Position" />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>城市：</label>
            <input type="text" v-model="formData.City" />
          </div>
          <div class="form-group">
            <label>期望薪资：</label>
            <input type="number" v-model="formData.Salary" />
          </div>
        </div>
      </section>

      <section>
        <h3>自我介绍</h3>
        <div class="form-group">
          <label>自我介绍：</label>
          <input type="text" v-model="formData.Introduction" />

          <!-- <textarea v-model="formData.Introduction"></textarea> -->
        </div>
      </section>

      <button type="submit" class="submit-button">提交</button>
    </form>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const baseURL = import.meta.env.VITE_APP_BASE_URL;

const formData = ref({
  ResumeID: null,
  Username: '',
  Gender: '',
  Email: '',
  Phone: '',
  Address: '',
  PostalCode: '',
  Education: '',
  Skills: '',
  JobType: '',
  Position: '',
  City: '',
  Salary: null,
  Introduction: '',
  PublishTime: null,
  Clicks: null
})

const fetchResume = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${baseURL}/getResume/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    if (response.data.resume) {
      Object.assign(formData.value, response.data.resume)
    }
    formData.value.Username = response.data.username
  } catch (error) {
    console.error('Failed to fetch resume:', error)
  }
}

onMounted(() => {
  fetchResume()
})

const handleSubmit = async () => {
  try {
    const response = await axios.post(`${baseURL}/updateResume/`, formData.value)
    if (response.status === 200) {
      alert('简历更新成功')
      router.push('/resume')
    }
  } catch (error) {
    if (error.response && error.response.status === 404) {
      try {
        const createResponse = await axios.post(`${baseURL}/createResume/`, formData.value)
        if (createResponse.status === 200) {
          alert('简历创建成功')
          router.push('/resume')
        }
      } catch (createError) {
        console.error('Failed to create resume:', createError)
        alert('简历创建失败，请稍后再试')
      }
    } else {
      console.error('Failed to update resume:', error)
      alert('简历更新失败，请稍后再试')
    }
  }
}
</script>

<style scoped>
.context {
  display: flex;
  background: linear-gradient(to bottom, rgba(116, 185, 255, 0.5), rgba(255, 255, 255, 0.8)); /* 修改整体背景颜色并加上透明度 */
  background: linear-gradient(135deg, #e0e7fa, #ffffff);
  
  background-attachment: fixed; /* 固定背景渐变 */
}

.resume-form {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 8px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 800px;
  margin: 0 auto;
  
  margin-top: 100px; /* 添加顶部间距 */
  /* border-color: #007bff; */
  /* border: 2px solid #ccc; */
  /* border: 3px solid #007bff; */
  border: 2px solid  rgba(0, 123, 255, 0.8);
}

.resume-form:hover {
  box-shadow: 8px 8px 8px rgba(0, 0, 0, 0.1);
  
  /* border-color: #007bff; */
}

section {
  /* margin-bottom: 30px; */
  padding: 20px;
  /* border: 1px solid #ddd; */
  border-radius: 10px;
}

h3 {
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.form-group {
  flex: 1;
  margin-bottom: 15px;
  margin-right: 20px; /* 添加右侧间距 */
}

input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  max-width: 500px; /* 添加最大宽度 */
  margin-bottom: 10px; /* 添加底部间距 */
}

.submit-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #0056b3;
}
</style>