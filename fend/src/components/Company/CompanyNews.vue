<template>
  <div class="company-news">
    <h2>企业新闻发布</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>新闻标题：</label>
        <input type="text" v-model="news.title" required />
      </div>
      <div class="form-group">
        <label>新闻内容：</label>
        <textarea v-model="news.content" rows="5" required></textarea>
      </div>
      <button type="submit">发布新闻</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const news = ref({
  title: '',
  content: ''
})

const handleSubmit = () => {
  // 这里添加发布新闻的逻辑
  alert('新闻已发布！')
}
</script>

<style scoped>
.company-news {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}
</style>