<template>
  <fileAllocating
    v-if="isShow"
    ref="allocating"
    @cancel="cancel"
  ></fileAllocating>
  <div class="context">
    <div class="manageJob">
      <h1>已发布职位管理</h1>
      <el-input v-model="searchQuery" placeholder="搜索职位..." class="search-input"></el-input>
      <el-select v-model="selectedCity" placeholder="选择城市" class="filter-select">
        <el-option label="取消选择" value=""></el-option>
        <el-option v-for="city in cities" :key="city" :label="city" :value="city"></el-option>
      </el-select>
      <el-select v-model="selectedPosition" placeholder="选择职位名称" class="filter-select">
        <el-option label="取消选择" value=""></el-option>
        <el-option v-for="position in positions" :key="position" :label="position" :value="position"></el-option>
      </el-select>
      <el-select v-model="selectedDepartment" placeholder="选择招聘部门" class="filter-select">
        <el-option label="取消选择" value=""></el-option>
        <el-option v-for="department in departments" :key="department" :label="department" :value="department"></el-option>
      </el-select>
      <div v-if="filteredJobs.length === 0">暂无发布的职位</div>
      <div v-else class="job-table-container">
        <table>
          <thead>
            <tr>
              <th>编号</th>
              <th>企业类型</th>
              <th>企业名称</th>
              <th>招聘部门</th>

              <th>职位名称</th>
              <!-- <th>职位描述</th> -->
              <th>城市</th>
              <th>薪资</th>
              <th>发布时间</th>
              <th>邮箱</th>
              <th>电话</th>
              <th>地址</th>
              <!-- <th>邮政编码</th> -->
              <th>职位空缺</th>
              <th>点击量</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(job, index) in filteredJobs" :key="job.JobID">
              <td>{{ index + 1 }}</td>
              <td>{{ job.EnterpriseType }}</td>
              <td>{{ job.EnterpriseName }}</td>
              <td>{{ job.HiringDepartment }}</td>

              <td>{{ job.Position }}</td>
              <!-- <td>{{ job.Description }}</td> -->
              <td>{{ job.City }}</td>
              <td>{{ job.Salary }}</td>
              <td>{{ job.PublishTime }}</td>

              <td>{{ job.Email }}</td>
              <td>{{ job.Phone }}</td>
              <td>{{ job.Address }}</td>
              <!-- <td>{{ job.PostalCode }}</td> -->
              <td>{{ job.Vacancies }}</td>
              <td>{{ job.Clicks }}</td>
              <td>
                <div class="button-group">
                  <el-button type="primary" @click="fetchApplicationDetails(job.EnterpriseName, job.HiringDepartment, job.Position)">详情</el-button>
                  <el-button type="warning" @click="openEditDialog(job)">修改</el-button>
                  <el-button type="danger" @click="deleteJob(job.JobID)">删除</el-button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <el-dialog v-model="dialogVisible" width="50%" @close="handleClose">
          <template #title>
            <h2>申请详情</h2>
          </template>
          <table class="detail-table">
            <thead>
              <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>申请日期</th>
                <th>状态</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(detail, index) in applicationDetails" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ detail.Name }}</td>
                <td>{{ detail.ApplicationDate }}</td>
                <td>{{ detail.ResponseResult }}</td>
              </tr>
            </tbody>
          </table>
        </el-dialog>
        <el-dialog v-model="editDialogVisible" width="50%" @close="handleEditClose">
          <template #title>
            <h2>修改职位</h2>
          </template>
          <el-form :model="editJobForm">
            <table class="edit-form-table">
              <tr>
                <td><el-form-item label="职位名称"><el-input v-model="editJobForm.Position"></el-input></el-form-item></td>
                <td><el-form-item label="职位描述"><el-input v-model="editJobForm.Description"></el-input></el-form-item></td>
              </tr>
              <tr>
                <td><el-form-item label="城市"><el-input v-model="editJobForm.City"></el-input></el-form-item></td>
                <td><el-form-item label="薪资"><el-input v-model="editJobForm.Salary"></el-input></el-form-item></td>
              </tr>
              <tr>
                <td><el-form-item label="企业类型"><el-input v-model="editJobForm.EnterpriseType"></el-input></el-form-item></td>
                <td><el-form-item label="邮箱"><el-input v-model="editJobForm.Email"></el-input></el-form-item></td>
              </tr>
              <tr>
                <td><el-form-item label="电话"><el-input v-model="editJobForm.Phone"></el-input></el-form-item></td>
                <td><el-form-item label="地址"><el-input v-model="editJobForm.Address"></el-input></el-form-item></td>
              </tr>
              <tr>
                <td><el-form-item label="邮政编码"><el-input v-model="editJobForm.PostalCode"></el-input></el-form-item></td>
                <td><el-form-item label="职位空缺"><el-input v-model="editJobForm.Vacancies"></el-input></el-form-item></td>
              </tr>
              <tr>
                <td colspan="2"><el-form-item label="招聘部门"><el-input v-model="editJobForm.HiringDepartment"></el-input></el-form-item></td>
              </tr>
            </table>
          </el-form>
          <template #footer>
            <el-button @click="handleEditClose">取消</el-button>
            <el-button type="primary" @click="updateJob">保存</el-button>
          </template>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ref, onMounted, computed } from 'vue';
import { ElInput, ElSelect, ElOption, ElButton, ElDialog, ElForm, ElFormItem } from 'element-plus';

export default {
  name: 'ManageReleasedJob',
  components: {
    ElInput,
    ElSelect,
    ElOption,
    ElButton,
    ElDialog,
    ElForm,
    ElFormItem
  },
  setup() {
    const baseURL = import.meta.env.VITE_APP_BASE_URL;
    const jobs = ref([]);
    const searchQuery = ref('');
    const selectedCity = ref('');
    const selectedPosition = ref('');
    const selectedDepartment = ref('');
    const cities = ref([]);
    const positions = ref([]);
    const departments = ref([]);
    const isShow = ref(true);
    const dialogVisible = ref(false);
    const applicationDetails = ref([]);
    const editDialogVisible = ref(false);
    const editJobForm = ref({
      JobID: '', // 添加 JobID 属性
    });

    const fetchJobs = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${baseURL}/CheckReleasedJob/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        jobs.value = response.data;
        cities.value = [...new Set(response.data.map(job => job.City))];
        positions.value = [...new Set(response.data.map(job => job.Position))];
        departments.value = [...new Set(response.data.map(job => job.HiringDepartment))];
      } catch (error) {
        console.error('Failed to fetch jobs:', error);
      }
    };

    const cancel = () => {
      isShow.value = false;
    };

    const filteredJobs = computed(() => {
      return jobs.value.filter(job => {
        return (
          job.Position.includes(searchQuery.value) &&
          (selectedCity.value === '' || job.City === selectedCity.value) &&
          (selectedPosition.value === '' || job.Position === selectedPosition.value) &&
          (selectedDepartment.value === '' || job.HiringDepartment === selectedDepartment.value)
        );
      });
    });

    const fetchApplicationDetails = async (enterpriseName, hiringDepartment, position) => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${baseURL}/applicationDetails/`, {
          headers: {
            Authorization: `Bearer ${token}`
          },
          params: {
            enterprise_name: enterpriseName,
            hiring_department: hiringDepartment,
            position: position
          }
        });
        applicationDetails.value = response.data;
        dialogVisible.value = true;
      } catch (error) {
        console.error('Failed to fetch application details:', error);
      }
    };

    const handleClose = () => {
      dialogVisible.value = false;
    };

    const openEditDialog = (job) => {
      editJobForm.value = { ...job };
      editDialogVisible.value = true;
    };

    const handleEditClose = () => {
      editDialogVisible.value = false;
    };

    const updateJob = async () => {
      try {
        const token = localStorage.getItem('token');
        await axios.put(`${baseURL}/updateReleasedJob/${editJobForm.value.JobID}`, {
          enterprise_type: editJobForm.value.EnterpriseType,
          email: editJobForm.value.Email,
          phone: editJobForm.value.Phone,
          address: editJobForm.value.Address,
          postal_code: editJobForm.value.PostalCode,
          position: editJobForm.value.Position,
          vacancies: editJobForm.value.Vacancies,
          city: editJobForm.value.City,
          description: editJobForm.value.Description,
          salary: editJobForm.value.Salary,
          hiring_department: editJobForm.value.HiringDepartment
        }, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        fetchJobs(); // 重新获取职位列表
        handleEditClose();
      } catch (error) {
        console.error('Failed to update job:', error);
      }
    };

    const editJob = (job) => {
      // 打开编辑对话框并填充职位信息
      // 这里可以实现打开一个编辑对话框，并填充职位信息
    };

    const deleteJob = async (jobId) => {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${baseURL}/deleteReleasedJob/${jobId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        fetchJobs(); // 重新获取职位列表
      } catch (error) {
        console.error('Failed to delete job:', error);
      }
    };

    onMounted(() => {
      fetchJobs();
    });

    return {
      jobs,
      searchQuery,
      selectedCity,
      selectedPosition,
      selectedDepartment,
      cities,
      positions,
      departments,
      filteredJobs,
      isShow,
      cancel,
      dialogVisible,
      applicationDetails,
      fetchApplicationDetails,
      handleClose,
      editJob,
      deleteJob,
      editDialogVisible,
      editJobForm,
      openEditDialog,
      handleEditClose,
      updateJob
    };
  },
};
</script>

<style scoped>
.context {
  background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));

  background-attachment: fixed;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}
.manageJob {
  width: 1500px;
  margin: 40px auto;
  padding: 40px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  /* font-family: 'Times New Roman', Times, serif; */
  line-height: 1.6;
}
.search-input {
  margin-bottom: 20px;
  width: 300px;
}
.filter-select {
  margin-bottom: 20px;
  width: 200px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: -50px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}

th {
  background-color: #00B4B3;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f1f1f1;
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
}

div {
  padding: 20px;
}

div[v-if] {
  text-align: center;
  font-size: 18px;
  color: #666;
}

.box-card {
  margin-bottom: 20px;
}

.job-table-container {
  display: flex;
  justify-content: space-between;
}
.application-details {
  display: none;
}
.detail-item {
  margin-bottom: 20px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 20px;
  background-color: #f9f9f9;
}

.detail-content p {
  margin: 0 0 10px;
  font-size: 16px;
  color: #333;
}

.detail-content p strong {
  color: #666;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0;
}

.detail-table th, .detail-table td {
  border: 1px solid #ebeef5;
  padding: 12px;
  text-align: center;
}

detail-table th {
  background-color: #007BFF;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.detail-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

detail-table tr:hover {
  background-color: #f1f1f1;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.edit-form-table {
  width: 100%;
  border-collapse: collapse;
}

.edit-form-table td {
  padding: 5px; /* 调整间距 */
  vertical-align: top;
}
</style>
