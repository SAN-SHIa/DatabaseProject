<template>
  <div class="login-container standalone-page">
    <div class="context">
      <h2>用户登录</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>选择角色：</label>
          <div class="role-selection">
            <button @click="selectRole('jobSeeker')" :class="{ active: formData.role === 'jobSeeker' }">
              <img src="@/assets/a.png" alt="求职者" class="role-logo" />
              我是求职者
            </button>
            <button @click="selectRole('recruiter')" :class="{ active: formData.role === 'recruiter' }">
              <img src="@/assets/b.png" alt="企业招聘者" class="role-logo" />
              我是招聘者
            </button>
            <button @click="selectRole('admin')" :class="{ active: formData.role === 'admin' }">
              <img src="@/assets/c.png" alt="超级管理员" class="role-logo" />
              我是管理员
            </button>
          </div>
        </div>
        <div class="form-group">
          <label>用户名：</label>
          <input
            type="text"
            v-model="formData.username"
            placeholder="请输入用户名"
            required
          />
        </div>
        <div class="form-group">
          <label>密码：</label>
          <input
            type="password"
            v-model="formData.password"
            placeholder="请输入密码"
            required

          />
        </div>

        <button type="submit" class="submit-button">登录</button>
        <div class="error-message" v-if="errorMessage">{{ errorMessage }}</div>
        <div class="links">
          <router-link to="/register">还没有账号？立即注册</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const formData = ref({
  username: '',
  password: '',
  role: ''
});
const errorMessage = ref('');
const baseURL = import.meta.env.VITE_APP_BASE_URL;

const selectRole = (role) => {
  formData.value.role = role;
};

const handleSubmit = async () => {
  try {
    let url = '';
    if (formData.value.role === 'jobSeeker') {
      url = `${baseURL}/login_user/`;
    } else if (formData.value.role === 'recruiter') {
      url = `${baseURL}/login_enterprise/`;
    } else if (formData.value.role === 'admin') {
      url = `${baseURL}/login_admin/`;
    }

    const response = await axios.post(url, {
      username: formData.value.username,
      password: formData.value.password
    });
    const token = response.data.access_token;
    localStorage.setItem('token', token);
    localStorage.setItem('role', formData.value.role); // 存储用户角色

    if (formData.value.role === 'jobSeeker') {
      router.push('/jobs');
    } else if (formData.value.role === 'recruiter') {
      router.push('/companyInfo');
    } else if (formData.value.role === 'admin') {
      router.push('/manageAllUsers');
    }
  } catch (error) {
    if (error.response && error.response.status === 400) {
      errorMessage.value = error.response.data.detail;
    } else {
      errorMessage.value = '登录失败，请稍后再试';
    }
  }
};
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #74b9ff, #0984e3);
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.context {
  width: 100%;
  max-width: 500px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  color: #ffffff;
  text-align: center;
  /* height: 200px; */
  animation: fadeIn 1s ease-in-out;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.form-group {
  margin-bottom: 20px;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

input, select {
  width: 475px;
  padding: 5px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: border 0.3s;
}

input:focus {
  border: 2px solid #74b9ff;
}

.submit-button {
  width: 100%;
  padding: 12px;
  font-size: 18px;
  background-color: #0984e3;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.submit-button:hover {
  background-color: #74b9ff;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.error-message {
  color: #ff6b6b;
  margin-top: 10px;
}

.links {
  margin-top: 15px;
}

.links a {
  color: #dfe6e9;
  text-decoration: none;
  font-weight: bold;
}

.links a:hover {
  text-decoration: underline;
}

.role-selection {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.role-selection button {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  margin: 0 5px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.role-selection button.active {
  background-color: #0984e3;
  color: #ffffff;
}

.role-selection button:not(.active) {
  background-color: #dfe6e9;
  color: #2d3436;
}

.role-selection button:hover:not(.active) {
  background-color: #b2bec3;
}

.role-selection button:hover {
  transform: translateY(-5px);
}

.role-selection button:hover .role-logo {
  transform: rotate(360deg);
}

.role-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  transition: transform 0.3s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>