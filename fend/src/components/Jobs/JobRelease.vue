<template>
  <div class="context">
    <div class="publish-job">
      <el-form :model="form" ref="formRef" label-width="120px">
        <el-form-item label="企业名称" prop="enterprise_name">
          <el-input v-model="form.enterprise_name" disabled></el-input>
        </el-form-item> 
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" disabled></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="form.address" disabled></el-input>
        </el-form-item>
        <el-form-item label="职位" prop="position">
          <el-input v-model="form.position"></el-input>
        </el-form-item>
        <el-form-item label="招聘部门" prop="hiring_department">
          <el-input v-model="form.hiring_department"></el-input>
        </el-form-item>
        <el-form-item label="城市" prop="city">
          <el-input v-model="form.city"></el-input>
        </el-form-item>
        <el-form-item label="薪资" prop="salary">
          <el-input v-model="form.salary"></el-input>
        </el-form-item>
        <el-form-item label="职位描述" prop="description">
          <el-input type="textarea" v-model="form.description"></el-input>
        </el-form-item>
        <el-form-item label="企业类型" prop="enterprise_type">
          <el-input v-model="form.enterprise_type"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="form.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮政编码" prop="postal_code">
          <el-input v-model="form.postal_code"></el-input>
        </el-form-item>
        <el-form-item label="职位空缺" prop="vacancies">
          <el-input v-model.number="form.vacancies" type="number"></el-input>
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
      enterprise_name: '',
      position: '',
      hiring_department: '',
      city: '',
      salary: '',
      description: '',
      enterprise_id: '',
      enterprise_type: '',
      email: '',
      phone: '',
      address: '',
      postal_code: '',
      vacancies: 0 // 确保职位空缺字段为数字类型
    });
    const formRef = ref(null);

    const submitForm = async () => {
      formRef.value.validate(async (valid) => {
        if (valid) {
          try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`${baseURL}/enterpriseReleaseJob/`, form.value, {
              headers: {
                'Authorization': `Bearer ${token}`
              }
            });
            ElMessage.success('发布成功！');
            console.log(response.data);
            form.value.position = '';
            form.value.hiring_department = '';
            form.value.city = '';
            form.value.salary = '';
            form.value.description = '';
            form.value.enterprise_type = '';
            form.value.phone = '';
            form.value.postal_code = '';
            form.value.vacancies = 0; // 清空职位空缺
            setTimeout(() => {
              window.location.reload();
            }, 50);
          } catch (error) {
            console.error('Failed to submit job:', error);
            ElMessage.error('发布失败，请重试！');
          }
        } else {
          console.log('表单验证失败');
          return false;
        }
      });
    };

    const resetForm = () => {
      form.value.position = '';
      form.value.hiring_department = '';
      form.value.city = '';
      form.value.salary = '';
      form.value.description = '';
      form.value.enterprise_type = '';
      form.value.phone = '';
      form.value.postal_code = '';
      form.value.vacancies = 0; // 清空职位空缺
      ElMessage.success('重置成功！');
    };

    const fetchCompanyInfo = async (username) => {
      try {
        const response = await axios.get(`${baseURL}/enterpriseInfo/${username}`);
        form.value.enterprise_name = response.data.EnterpriseName;
        form.value.enterprise_id = response.data.EnterpriseID;
        form.value.enterprise_type = response.data.EnterpriseType;
        form.value.email = response.data.Email;
        form.value.phone = response.data.Phone;
        form.value.address = response.data.Address;
        form.value.postal_code = response.data.PostalCode;
        form.value.vacancies = response.data.Vacancies;
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
.context {
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  background: linear-gradient(135deg, #e0e7fa, #ffffff);
  background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));
  padding: 20px;
}

.publish-job {
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
