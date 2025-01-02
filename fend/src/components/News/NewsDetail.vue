<template>
    <div class="context">
        <div class="news-detail">
            <h1 class="news-title">{{ news.Title }}</h1>
            <div class="news-meta">
            <span class="news-date">时间: {{ formatDate(news.Publish_time) }}</span>
            <span class="news-views">点击数: {{ news.Views }}</span>
            <!-- <span class="news-share">分享到: 
                <img src="/icons/wechat-icon.png" alt="WeChat" class="share-icon" />
                <img src="/icons/weibo-icon.png" alt="Weibo" class="share-icon" />
            </span> -->
            </div>
            <div class="news-content">
            <p>{{ news.Content }}</p>
            <img v-if="news.Image" :src="news.Image" alt="News Image" class="news-image" />
            </div>
        </div>
    </div>
</template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRoute } from 'vue-router';
  
  const baseURL = import.meta.env.VITE_APP_BASE_URL;
  const route = useRoute();
  const news = ref({});
  
  onMounted(async () => {
    try {
      const response = await axios.get(`${baseURL}/news/${route.params.newsId}`);
      news.value = response.data;
    } catch (error) {
      console.error('Failed to fetch news detail:', error);
    }
  });
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
  };
  </script>
  
  <style scoped>
  .context {
    min-height: 100vh;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    background: linear-gradient(135deg, #f0f4f8, #ffffff);
    padding: 20px;
  }
  .news-detail {
    width: 900px;
    margin: 100px auto;
    padding: 30px;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  .news-title {
    font-size: 32px;
    font-weight: bold;
    color: #333;
    margin-bottom: 20px;
    text-align: center;
  }
  .news-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 16px;
    color: #666;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 10px;
  }
  .news-meta .share-icon {
    width: 20px;
    height: 20px;
    margin-left: 5px;
    cursor: pointer;
  }
  .news-content {
    font-size: 18px;
    line-height: 1.8;
    color: #444;
  }
  .news-content .news-image {
    width: 100%;
    height: auto;
    margin-top: 20px;
    border-radius: 8px;
  }
  </style>