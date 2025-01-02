<template>
  <div class = "context">
  <div class="publish-news">
    <el-form :model="form" ref="formRef" label-width="120px">
      <el-form-item label="来源" prop="source">
        <el-input v-model="form.source" disabled></el-input>
      </el-form-item>
      
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title"></el-input>
      </el-form-item>
      <el-form-item label="内容" prop="content">
        <el-input type="textarea" v-model="form.content"></el-input>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="submitForm">发布</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';

export default {
  setup() {
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const form = ref({
      title: '',
      content: '',
      source: '',
      enterprise_id: '' // 新增字段
    });
    const formRef = ref(null);

    const submitForm = async () => {
      formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${baseURL}/enterprisePostNews/`, form.value, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            ElMessage.success('发布成功！');
            console.log(response.data);
            form.value.title = ''; // 清空标题
            form.value.content = ''; // 清空内容
          } catch (error) {
            console.error('Failed to submit news:', error);
            ElMessage.error('发布失败，请重试！');
          }
        } else {
          console.log('表单验证失败');
          return false;
        }
      });
    };

    const resetForm = () => {
      form.value.title = '';
      form.value.content = '';
    };

    const fetchCompanyInfo = async (username) => {
      try {
        const response = await axios.get(`${baseURL}/enterpriseInfo/${username}`);
        form.value.source = response.data.EnterpriseName;
        form.value.enterprise_id = response.data.EnterpriseID; // 获取 EnterpriseID
      } catch (error) {
        console.error('Failed to fetch enterprise info:', error);
      }
    };

    onMounted(async () => {
      try {
        const token = localStorage.getItem('token');
        const userResponse = await axios.get(`${baseURL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const username = userResponse.data.username;
        await fetchCompanyInfo(username);
      } catch (error) {
        console.error('获取用户信息失败', error);
      }
    });

    return {
      form,
      formRef,
      submitForm,
      resetForm
    };
  }
};
</script>

<style scoped>
.context{
  min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));


    padding: 20px;

}

.publish-news {
  width: 900px;
  margin: 40px auto;
  padding: 40px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 0;
  box-shadow: none;
  font-family: 'Times New Roman', Times, serif;
  line-height: 1.6;
  margin-top: 100px;
}
.el-form-item {
  margin-bottom: 20px;
}
.el-input {
  border-radius: 0;
  border: 1px solid #ddd;
}
.el-button {
  border-radius: 0;
  background-color: #000;
  color: #fff;
  border: none;
}
.el-button:hover {
  background-color: #444;
}
</style>
