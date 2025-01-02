<template>
  <el-container class="bg">
    <el-main class="application-container">
      <el-row class="button-container" justify="space-between">
        <div>
          <el-button type="warning" @click="filterApplications('未读')">待办</el-button>
          <el-button type="success" @click="filterApplications('通过')">通过</el-button>
          <el-button type="danger" @click="filterApplications('拒绝')">拒绝</el-button>
          <el-button type="primary" @click="filterApplications('全部')">总览</el-button>
        </div>
        <el-button type="primary" @click="toggleEditMode">{{ editMode ? '退出编辑模式' : '进入编辑模式' }}</el-button>
      </el-row>
      
      <el-row class="content-container" :gutter="20">
        <el-col :span="12" class="scrollable-content">
          <el-card v-for="application in filteredApplications" :key="application.ApplicationID" class="application-item" @click="showResume(application.UserID)">
            <div class="application-content">
              <div class="application-date">
                <el-tag type="info" class="date-circle">
                  <div class="date-day-month">{{ formatDayMonth(application.ApplicationDate) }}</div>
                  <div class="date-month-year">{{ formatYear(application.ApplicationDate) }}</div>
                </el-tag>
              </div>
              <div class="application-details">
                <p class="application-title">{{ application.Name }} —— {{ application.EnterpriseName }} | {{ application.HiringDepartment }} | {{ application.Position }}</p>
                <el-row class="status-container" align="middle">
                  <el-badge :value="application.ResponseResult" :type="getStatusType(application.ResponseResult)" class="status-indicator"></el-badge>
                  <p class="status-text">{{ application.EnterpriseMessage }}</p>
                </el-row>
              </div>
            </div>
            <div v-if="editMode" class="edit-options">
              <el-button type="danger" @click.stop="deleteApplication(application.ApplicationID)">删除</el-button>
            </div>
            <div v-if="selectedResume && selectedResume.UserID === application.UserID && filterType === '未读'" class="enterprise-response">
              <el-form :model="responseForm">
                <el-form-item label="审批结果">
                  <el-radio-group v-model="responseForm.result">
                    <el-radio label="通过">通过</el-radio>
                    <el-radio label="拒绝">拒绝</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="留言信息">
                  <el-input type="textarea" v-model="responseForm.message"></el-input>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="submitResponse(application.ApplicationID)">确认</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-card>
        </el-col>
        <el-col v-if="selectedResume" :span="12">
          <el-card class="resume-container">
            <h3>简历详情</h3>
            <div class="info">
              <p><span>用户名:</span> {{ selectedResume.Username }}</p>
              <p><span>性别:</span> {{ selectedResume.Gender }}</p>
              <p><span>邮箱:</span> {{ selectedResume.Email }}</p>
              <p><span>电话:</span> {{ selectedResume.Phone }}</p>
              <p><span>地址:</span> {{ selectedResume.Address }}</p>
              <p><span>邮政编码:</span> {{ selectedResume.PostalCode }}</p>
              <p><span>学历:</span> {{ selectedResume.Education }}</p>
              <p><span>技能:</span> {{ selectedResume.Skills }}</p>
              <p><span>工作类型:</span> {{ selectedResume.JobType }}</p>
              <p><span>职位:</span> {{ selectedResume.Position }}</p>
              <p><span>城市:</span> {{ selectedResume.City }}</p>
              <p><span>薪资:</span> {{ selectedResume.Salary }}</p>
              <p><span style="font-weight: 600; color: #333;">简介:</span> {{ selectedResume.Introduction }}</p>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  setup() {
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const applications = ref([]);
    const editMode = ref(false);
    const selectedResume = ref(null);
    const filteredApplications = ref([]);
    const filterType = ref('全部');
    const responseForm = ref({
      result: '',
      message: ''
    });

    const fetchApplications = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }
        const response = await axios.get(`${baseURL}/enterpriseManageApply/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        applications.value = response.data;
      } catch (error) {
        ElMessage.error('Error fetching applications: ' + error.message);
      }
    };

    const formatDayMonth = (dateString) => {
      const date = new Date(dateString);
      const day = date.getDate().toString().padStart(2, '0');
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      return `${month}-${day}`;
    };

    const formatYear = (dateString) => {
      const date = new Date(dateString);
      return date.getFullYear();
    };

    const getStatusType = (status) => {
      switch (status) {
        case '通过':
          return 'success';
        case '拒绝':
          return 'danger';
        case '未读':
          return 'info';
        default:
          return '';
      }
    };

    const toggleEditMode = () => {
      editMode.value = !editMode.value;
    };

    const deleteApplication = async (applicationID) => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }
        await axios.delete(`${baseURL}/revokeApply/${applicationID}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        applications.value = applications.value.filter(app => app.ApplicationID !== applicationID);
        ElMessage.success('Application deleted successfully');
      } catch (error) {
        ElMessage.error('Error deleting application: ' + error.message);
      }
    };

    const showResume = async (UserID) => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }
        const response = await axios.get(`${baseURL}/enterpriseCheckResume/${UserID}`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        selectedResume.value = response.data.resume;
      } catch (error) {
        ElMessage.error('Error fetching resume: ' + error.message);
      }
    };

    const filterApplications = (type) => {
      filterType.value = type;
      if (type === '全部') {
        filteredApplications.value = applications.value;
      } else {
        filteredApplications.value = applications.value.filter(app => app.ResponseResult === type);
      }
    };

    const submitResponse = async (applicationID) => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          throw new Error('Token not found');
        }
        const response = await axios.post(`${baseURL}/enterpriseResponse/${applicationID}`, {
          ResponseResult: responseForm.value.result,
          EnterpriseMessage: responseForm.value.message
        }, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        ElMessage.success('Response submitted successfully');
        fetchApplications();
      } catch (error) {
        ElMessage.error('Error submitting response: ' + error.message);
      }
    };

    onMounted(() => {
      fetchApplications().then(() => {
        filterApplications('全部');
      });
    });

    return {
      applications,
      editMode,
      fetchApplications,
      formatDayMonth,
      formatYear,
      getStatusType,
      toggleEditMode,
      deleteApplication,
      selectedResume,
      showResume,
      filteredApplications,
      filterApplications,
      responseForm,
      submitResponse,
      filterType
    };
  }
};
</script>

<style scoped>
.bg {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));

  padding: 20px;
}

.application-container {
  width: 90%;
  max-width: 1200px;
  padding: 30px;
  font-family: 'Roboto', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  background-color: #ffffff;
  border: 2px solid rgba(0, 180, 179, 0.8);
}

.button-container {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

.scrollable-content {
  max-height: 500px;
  overflow-y: auto;
}

.date-circle {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(0, 180, 179, 0.8);
  color: #ffffff;
  font-size: 14px;
  font-weight: bold;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-left: -10px;
}

.date-day-month {
  font-size: 16px;
  font-weight: bold;
  text-align: center; /* 设置为居中 */
}

.date-month-year {
  font-size: 16px;
  text-align: center; /* 设置为居中 */
}
.application-content {
  padding: 15px;
  display: flex;
  gap: 20px; /* 添加距离 */
}

.application-details {
  flex: 1;
}

.application-title {
  font-weight: bold;
  margin-bottom: 8px;
  color: #007bff;
}

.application-content p {
  margin: 0 0 8px;
  color: #333;
}

.status-container {
  display: flex;
  align-items: center;
  margin-top: 16px;
}

.status-indicator {
  margin-right: 8px;
}

.edit-options {
  margin-top: 10px;
}

.application-item {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.application-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.resume-container {
  padding: 20px;
  border: 1px solid #ebedf0;
  border-radius: 8px;
  background-color: #f9f9fb;
  max-height: 500px;
  overflow-y: auto;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.resume-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

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

.enterprise-response {
  margin-top: 20px;
}

@media (max-width: 600px) {
  .content-container {
    flex-direction: column;
  }

  .application-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .application-content {
    padding: 10px;
  }

  .edit-options {
    margin: 10px;
  }

  .info {
    grid-template-columns: 1fr;
  }
}
</style>