<template>
  <div class="context">
    <div class="news-container">
      <div class="search-container">
        <input v-model="searchParams.keyword" class="search-input" placeholder="输入新闻标题或内容" />
        <input v-model="searchParams.source" class="search-input" placeholder="输入新闻来源" />
        <button @click="handleSearch" class="search-button">搜索</button>
      </div>
      <div class="news-list">
        <div v-for="news in filteredNewsList" :key="news.NewsID" class="news-item" @click="goToNewsDetail(news.NewsID)">
          <div class="news-date">
            <div class="date-circle">
              <span class="date-day">{{ formatDay(news.Publish_time) }}</span>
              <span class="date-month-year">{{ formatMonthYear(news.Publish_time) }}</span>
            </div>
          </div>
          <div class="news-content">
            <h3 class="news-title">{{ news.Title }}</h3>
            <p class="news-summary">{{ truncateContent(news.Content) }}</p>
          </div>
          <div class="read-more">阅读全文</div>
          <el-button type="danger" class="delete-button" @click.stop="deleteNews(news.NewsID)">删除</el-button>
        </div>
      </div>
    </div>
    <div class="floating-button" @click="goToPostNews">
      <el-button type="primary" icon="el-icon-plus">发布新闻</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';

const baseURL = import.meta.env.VITE_APP_BASE_URL;

const newsList = ref([]);
const searchParams = ref({
  keyword: '',
  source: ''
});
const router = useRouter();

const fetchNewsList = async () => {
  try {
    const response = await axios.get(`${baseURL}/newsList/`);
    newsList.value = response.data;
  } catch (error) {
    console.error('Failed to fetch news:', error);
    ElMessage.error('获取新闻列表失败');
  }
};

onMounted(fetchNewsList);

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

const truncateContent = (content) => {
  return content.length > 100 ? content.substring(0, 100) + '...' : content;
};

const goToNewsDetail = async (newsId) => {
  try {
    await axios.post(`${baseURL}/news/${newsId}/increment_views`);
  } catch (error) {
    console.error('Failed to increment views:', error);
  }
  router.push({ name: 'NewsDetail', params: { newsId } });
};

const handleSearch = () => {
  fetchNewsList();
};

const deleteNews = async (newsId) => {
  try {
    await axios.delete(`${baseURL}/manageNews/${newsId}`);
    ElMessage.success('新闻删除成功');
    fetchNewsList();
  } catch (error) {
    console.error('Failed to delete news:', error);
    ElMessage.error('删除新闻失败');
  }
};

const goToPostNews = () => {
  router.push({ path: '/postAdminNews' });
};

const filteredNewsList = computed(() => {
  return newsList.value.filter(news => {
    return (
      (news.Title.toLowerCase().includes(searchParams.value.keyword.toLowerCase()) ||
      news.Content.toLowerCase().includes(searchParams.value.keyword.toLowerCase())) &&
      news.Source.toLowerCase().includes(searchParams.value.source.toLowerCase())
    );
  });
});
</script>

<style scoped>
.context {
  display: flex;
  flex-direction: column;
  background: linear-gradient(to bottom, rgba(255, 126, 95, 0.1), rgba(254, 180, 123, 0.5));
  min-height: 100vh;
}

.search-container {
  display: flex;
  justify-content: center;
  margin-top: 50px;
  /* padding: 20px; */
}

.search-input {
  flex: 1;
  margin-right: 10px;
  padding: 10px;
  border: 2px solid #ff8c00;
  border-radius: 4px;
  margin-bottom: 20px;
}

.search-button {
  padding: 10px 20px;
  background-color: #ff8c00;
  color: white;
  border: 2px solid #e07b00;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;

}

.search-button:hover {
  background-color: #e07b00;
}

.news-container {
  max-width: 900px;
  margin: 0 auto;
  margin-top: 20px;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.news-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.news-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #f5faff;
  border: 1px solid #ddd;
  border-radius: 5px;
  overflow: hidden;
  transition: background-color 0.3s, color 0.3s;
  position: relative;
}

.news-item:hover {
  background-color: #e07b00;
  color: #fff;
}

.news-item:hover .news-title,
.news-item:hover .news-summary {
  color: #fff;
}

.news-item:hover .date-day,
.news-item:hover .date-month-year {
  color: #e07b00;
}

.news-item:hover .date-circle {
  background-color: #fff;
}

.news-item:hover .read-more {
  opacity: 1;
  right: 10px;
}

.news-date {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 15px;
  min-width: 80px;
}

.date-circle {
  background-color: #e07b00;
  color: #fff;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  transition: background-color 0.3s, color 0.3s;
}

.date-day {
  font-size: 24px;
  font-weight: bold;
}

.date-month-year {
  font-size: 14px;
}

.news-content {
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.news-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0 0 10px;
  color: #333;
  transition: color 0.3s;
}

.news-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  transition: color 0.3s;
}

.read-more {
  position: absolute;
  right: -100px;
  top: 20%;
  transform: translateY(-50%);
  background-color: #e07b00;
  color: #fff;
  font-weight: bold;
  padding: 5px 10px;
  border-radius: 3px;
  transition: right 0.3s, opacity 0.3s;
  opacity: 0;
}

.delete-button {
  margin-right: 15px;
  background-color: #ff4d4f;
  border: 2px solid #d9363e;
}

.delete-button:hover {
  background-color: #d9363e;
}

.floating-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
  font-size: 18px;
}
</style>