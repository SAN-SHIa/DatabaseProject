<template>
  <div class="context">
    <div class="manageInfo">
      <h1>账号信息管理</h1>
      <div class="button-group left-align">
        <el-button :class="{ active: view === 'users' }" @click="view = 'users'">查看用户</el-button>
        <el-button :class="{ active: view === 'enterprises' }" @click="view = 'enterprises'">查看企业</el-button>
      </div>
      <div v-if="view === 'users'">
        <!-- <h2>所有用户信息</h2> -->
        <table>
          <thead>
            <tr>
              <th>UserID</th>
              <th>Username</th>
              <th>Password</th>
              <th>Name</th>
              <th>Email</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.UserID">
              <td>{{ user.UserID }}</td>
              <td>{{ user.Username }}</td>
              <td>{{ user.Password }}</td>
              <td>{{ user.Name }}</td>
              <td>{{ user.Email }}</td>
              <td>
                <el-button @click="confirmDeleteUser(user.UserID)">删除</el-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="view === 'enterprises'">
        <!-- <h2>所有企业信息</h2> -->
        <table>
          <thead>
            <tr>
              <th>EnterpriseID</th>
              <th>EnterpriseName</th>
              <th>Username</th>
              <th>Password</th>
              <th>Address</th>
              <th>Email</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="enterprise in enterprises" :key="enterprise.EnterpriseID">
              <td>{{ enterprise.EnterpriseID }}</td>
              <td>{{ enterprise.EnterpriseName }}</td>
              <td>{{ enterprise.Username }}</td>
              <td>{{ enterprise.Password }}</td>
              <td>{{ enterprise.Address }}</td>
              <td>{{ enterprise.Email }}</td>
              <td>
                <el-button @click="confirmDeleteEnterprise(enterprise.EnterpriseID)">删除</el-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

const baseURL = import.meta.env.VITE_APP_BASE_URL;

export default {
  data() {
    return {
      view: 'users',
      users: [],
      enterprises: []
    };
  },
  created() {
    this.fetchUsers();
    this.fetchEnterprises();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get(`${baseURL}/allUsers/`);
        this.users = response.data;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async fetchEnterprises() {
      try {
        const response = await axios.get(`${baseURL}/allEnterprises/`);
        this.enterprises = response.data;
      } catch (error) {
        console.error('Error fetching enterprises:', error);
      }
    },
    confirmDeleteUser(userId) {
      if (confirm('确定要删除这个用户吗？')) {
        this.deleteUser(userId);
      }
    },
    confirmDeleteEnterprise(enterpriseId) {
      if (confirm('确定要删除这个企业吗？')) {
        this.deleteEnterprise(enterpriseId);
      }
    },
    async deleteUser(userId) {
      try {
        await axios.delete(`${baseURL}/deleteUser/${userId}`);
        this.fetchUsers();
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    },
    async deleteEnterprise(enterpriseId) {
      try {
        await axios.delete(`${baseURL}/deleteEnterprise/${enterpriseId}`);
        this.fetchEnterprises();
      } catch (error) {
        console.error('Error deleting enterprise:', error);
      }
    }
  }
};
</script>

<style scoped>
.context {
  background: linear-gradient(to bottom, rgba(255, 126, 95, 0.1), rgba(254, 180, 123, 0.5));
   /* 修改整体背景颜色并加上透明度 */
  background-attachment: fixed;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 50px;
}
.manageInfo {
  width: 1500px;
  margin: 40px auto;
  padding: 40px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Times New Roman', Times, serif;
  line-height: 1.6;
}
.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}
.button-group.left-align {
  justify-content: flex-start;
}
.button-group .el-button.active {
  background-color: #ff7e5f;
  color: white;
  border: 1px solid #feb47b;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  box-shadow: 0 2px 3px rgba(0, 0, 0, 0.1);
}
th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: center;
}
th {
  background-color: #ff7e5f;
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
h1, h2 {
  color: #333;
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: 600;
}
</style>
