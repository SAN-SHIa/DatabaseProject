<template>
  <header class="header">
    <h1>SANSHI招聘</h1>
    <div class="nav-links"> 
      <router-link to="/jobs" v-if="userRole === 'jobSeeker'">找工作</router-link>
      <router-link to="/newsEp" v-if="userRole === 'recruiter'">行业新闻</router-link>
      
      <router-link to="/news" v-if="userRole === 'jobSeeker'">行业新闻</router-link>
      <router-link to="/resume" v-if="userRole === 'jobSeeker'">更新简历</router-link>
      <router-link to="/myApply" v-if="userRole === 'jobSeeker'">我的申请</router-link>

      <router-link to="/JobRelease" v-if="userRole === 'recruiter'">发布招聘</router-link>
      <router-link to="/ManageReleasedJob" v-if="userRole === 'recruiter'">招聘管理</router-link>

      <router-link to="/epPublishNews" v-if="userRole === 'recruiter'">发布新闻</router-link>
      <router-link to="/epManageApply" v-if="userRole === 'recruiter'">收件箱</router-link>
      <router-link to="/companyInfo" v-if="userRole === 'recruiter'">公司信息</router-link>

      <router-link to="/manageAllJobs" v-if="userRole === 'admin'">已发布职位管理</router-link>
      <router-link to="/manageAllnews" v-if="userRole === 'admin'">已发布新闻管理</router-link>
      <router-link to="/manageAllUsers" v-if="userRole === 'admin'">用户管理</router-link>
      <router-link to="/postAdminNews" v-if="userRole === 'admin'">发布系统新闻</router-link>
    </div>
    <nav>
      <div v-if="isLoggedIn" class="user-info">
        你好，{{ username }}
        <button @click="logout">退出登录</button>
      </div>
      <div v-else class="auth-links">
        <router-link to="/login">登录</router-link>
        <router-link to="/register">注册</router-link>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const isLoggedIn = ref(false);
const username = ref('');
const router = useRouter();

onMounted(() => {
  const token = localStorage.getItem('token');
  if (token) {
    const payload = JSON.parse(atob(token.split('.')[1]));
    username.value = payload.sub;
    isLoggedIn.value = true;
  }
});

const userRole = localStorage.getItem('role'); // 获取用户角色

const headerBackground = computed(() => {
  switch (userRole) {
    case 'jobSeeker':
      return 'linear-gradient(120deg, #3f72af 0%, #66a6ff 100%)';
    case 'recruiter':
      return 'linear-gradient(120deg, #00B4B3 0%, #009E9D 100%)';

    case 'admin':
      return 'linear-gradient(120deg, #ff7e5f 0%, #feb47b 100%)';

    default:
      return 'linear-gradient(120deg, #3f72af 0%, #66a6ff 100%)';
  }
});

const logout = () => {
  localStorage.removeItem('token');
  isLoggedIn.value = false;
  username.value = '';
  router.push('/login');
};
</script>

<style scoped>
.header {
  background: v-bind(headerBackground);
  /* background: linear-gradient(120deg, #3f72af 0%, #66a6ff 100%); */
  /* background-color: #007bff; */
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* 固定header */
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
}

body {
  padding-top: 80px; 
  /* 确保内容不会被固定的header遮挡 */
}

h1 {
  font-size: 24px;
  margin: 0;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 16px;
  transition: color 0.3s;
}

.nav-links a:hover {
  color: #ffdd57;
}

nav {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-right: 30px;
}

.auth-links {
  display: flex;
  gap: 15px;
  /* margin-right: 20px; */
}

button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 16px;
  transition: color 0.3s;
}

button:hover {
  color: #ffdd57;
  text-decoration: underline;
}
</style>