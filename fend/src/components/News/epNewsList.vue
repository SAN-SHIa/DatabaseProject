<template>
    <div class = "context">
    <div class="news-container">
      <div class="news-list">
        <div v-for="news in newsList" :key="news.NewsID" class="news-item" @click="goToNewsDetail(news.NewsID)">
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
        </div>
      </div>
    </div>
  </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const baseURL = import.meta.env.VITE_APP_BASE_URL;
  const newsList = ref([]);
  const router = useRouter();
  
  onMounted(async () => {
    try {
      const response = await axios.get(`${baseURL}/newsList/`);
      newsList.value = response.data;
    } catch (error) {
      console.error('Failed to fetch news:', error);
    }
  });
  
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
  </script>
  
  <style scoped>
  .context {
    /* min-height: 100vh; */
    display: flex;
    /* align-items: center; */
    /* justify-content: center; */
    background: linear-gradient(to bottom, rgba(0, 180, 179, 0.1), rgba(0, 247, 246, 0.05));

    /* padding: 20px; */
  }
  .news-container {
    max-width: 900px;
    margin: 0 auto;
    margin-top: 100px;
    padding: 20px;
    font-family: Arial, sans-serif;
    /* { */
  /* } */
  }
  
  .news-list {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  .news-item {
    display: flex;
    background-color: #f5faff;
    /* border: 1px solid rgba(0, 180, 179, 0.5);  */
    /* 修改后的边框颜色 */
    border-radius: 5px;
    overflow: hidden;
    transition: background-color 0.3s, color 0.3s;
    position: relative;
  }
  
  .news-item:hover {
    background-color: rgba(0, 180, 179, 0.8); /* 修改后的填充颜色 */
    color: #fff;
  }
  
  .news-item:hover .news-title,
  .news-item:hover .news-summary{
    color: #fff;
  }
  .news-item:hover .date-day,
  .news-item:hover .date-month-year {
    color: rgba(0, 180, 179, 0.8);
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
    background-color: rgba(0, 180, 179, 0.8); /* 修改后的填充颜色 */
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
    background-color: rgba(0, 180, 179, 0.8); /* 修改后的按钮颜色 */
    color: #fff;
    font-weight: bold;
    padding: 5px 10px;
    border-radius: 3px;
    transition: right 0.3s, opacity 0.3s;
    opacity: 0;
  }
  </style>