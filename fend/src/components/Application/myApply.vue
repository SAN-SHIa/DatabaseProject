<template>
  <div class="bg">
      <div class="application-container">
          <div class="button-container">
              <button class="edit-mode-button" @click="toggleEditMode">{{ editMode ? '退出编辑模式' : '进入编辑模式' }}</button>
          </div>
          <div class="application-list">
              <div v-for="application in applications" :key="application.ApplicationID" class="application-item">
                  <div class="application-date">
                      <div class="date-circle">
                          <span class="date-day">{{ formatDay(application.ApplicationDate) }}</span>
                          <span class="date-month-year">{{ formatMonthYear(application.ApplicationDate) }}</span>
                      </div>
                  </div>
                  <div class="application-content">
                      <p style="font-weight: bold;"> {{ application.EnterpriseName }}|{{ application.HiringDepartment }}|{{ application.Position }}</p>
                      <div class="status-container">
                        <div class="status-indicator" :class="getStatusClass(application.ResponseResult)"></div>
                        <p class="status-text"> {{ application.ResponseResult }}</p>
                      </div>
                      <p class="enterprise-message">{{ application.EnterpriseMessage }}</p> <!-- 新增的展示EnterpriseMessage的代码 -->
                  </div>
                  <div v-if="editMode" class="edit-options">
                      <button @click="deleteApplication(application.ApplicationID)">删除</button>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
setup() {
  const baseURL = import.meta.env.VITE_APP_BASE_URL;
  const applications = ref([]);
  const editMode = ref(false);

  const fetchApplications = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Token not found');
      }
      const response = await axios.get(`${baseURL}/myApply/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      applications.value = response.data;
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const formatDay = (dateString) => {
    const date = new Date(dateString);
    return date.getDate().toString().padStart(2, '0');
  };

  const formatMonthYear = (dateString) => {
    const date = new Date(dateString);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${year}-${month}`;
  };

  const getStatusClass = (status) => {
    switch (status) {
      case '通过':
        return 'status-approved';
      case '拒绝':
        return 'status-rejected';
      case '未读':
        return 'status-unread';
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
    } catch (error) {
      console.error('Error deleting application:', error);
    }
  };

  onMounted(() => {
    fetchApplications();
  });

  return {
    applications,
    editMode,
    fetchApplications,
    formatDay,
    formatMonthYear,
    getStatusClass,
    toggleEditMode,
    deleteApplication
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
  background: linear-gradient(135deg, #eef2f7, #ffffff);
  padding: 20px;
}

.application-container {
  width: 90%;
  max-width: 800px;
  margin-top: 80px;
  padding: 30px;
  font-family: 'Microsoft YaHei', sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-radius: 12px;
  background-color: #ffffff;
  border: 2px solid  rgba(0, 123, 255, 0.8);
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.edit-mode-button {
  background-color: #409eff;
  color: #fff;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-mode-button:hover {
  background-color: #66b1ff;
}

.application-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.application-item {
  display: flex;
  align-items: center;
  background-color: #f9f9fb;
  border: 1px solid #ebedf0;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
}

.application-item:hover {
  transform: translateY(-2px);
}

.application-date {
  padding: 10px 15px;
}

.date-circle {
  background-color: #409eff;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

.date-day {
  font-size: 22px;
  font-weight: bold;
}

.date-month-year {
  font-size: 12px;
}

.application-content {
  flex: 1;
  padding: 15px;
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
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 8px;
  margin-top: -5px;
}

.status-approved {
  background-color: #67c23a;
}

.status-rejected {
  background-color: #f56c6c;
}

.status-unread {
  background-color: #909399;
}

.edit-options {
  margin-right: 15px;
}

.edit-options button {
  background-color: #f56c6c;
  color: #fff;
  border: none;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-options button:hover {
    background-color: #fa8c8c;
}

.enterprise-message {
  margin-top: 8px;
  color: #666;
}

@media (max-width: 600px) {
  .application-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .application-date {
    padding: 10px;
  }

  .application-content {
    padding: 10px;
  }

  .edit-options {
    margin: 10px;
  }
}
</style>