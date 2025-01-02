import { createRouter, createWebHistory } from 'vue-router'
import LoginForm from '../components/Auth/LoginForm.vue'
import RegisterForm from '../components/Auth/RegisterForm.vue'
import ResumeForm from '../components/Profile/ResumeForm.vue'
// import JobPreferences from '../components/Profile/JobPreferences.vue'
import JobApplication from '../components/Jobs/JobApplication.vue'

import NewsList from '../components/News/NewsList.vue'
import NewsDetail from '../components/News/NewsDetail.vue'
import epPublishNews from '@/components/News/epPublishNews.vue'

import CompanyInfo from '../components/Company/CompanyInfo.vue'
import CompanyNews from '../components/Company/CompanyNews.vue'
// import JobPosting from '../components/Company/JobPosting.vue'
import ApplicantList from '../components/Company/ApplicantList.vue'
// import JobSeekerManagement from '../components/Company/JobSeekerManagement.vue'

import JobList from '../components/Jobs/JobList.vue'
import JobDetail from '../components/Jobs/JobDetail.vue'
import JobRelease from '@/components/Jobs/JobRelease.vue'
import ManageReleasedJob from '@/components/Jobs/ManageReleasedJob.vue'

import myApply from '../components/Application/myApply.vue'  //12-7写这个   
import epManageApply from '../components/Application/epManageApply.vue'

import manageAllJobs from '@/components/Admin/manageAllJobs.vue'
import manageAllnews from '@/components/Admin/manageAllNews.vue'
import manageAllUsers from '@/components/Admin/manageAllUsers.vue'
import postAdminNews from '@/components/Admin/postAdminNews.vue'

import epNewsList from '@/components/News/epNewsList.vue'
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginForm
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterForm
  },
  {
    path: '/resume',
    name: 'Resume',
    component: ResumeForm
  },
  // {
  //   path: '/preferences',
  //   name: 'JobPreferences',
  //   component: JobPreferences
  // },
  {
    path: '/jobs',
    name: 'Jobs',
    component: JobList
  },
  {
    path: '/apply/:jobId',
    name: 'JobApplication',
    component: JobApplication
  },
  {
    path: '/news',
    name: 'News',
    component: NewsList
  },
  {
    path: '/companyInfo',
    name: 'CompanyInfo',
    component: CompanyInfo
  },
  {
    path: '/company-news',
    name: 'CompanyNews',
    component: CompanyNews
  },
  
/*12-7写这个*/
  // {
  //   path: '/job-posting',
  //   name: 'JobPosting',
  //   component: JobPosting
  // },

  {
    path: '/applicant-list',
    name: 'ApplicantList',
    component: ApplicantList
  },
  // {
  //   path: '/job-seeker-management',
  //   name: 'JobSeekerManagement',
  //   component: JobSeekerManagement
  // },
  {
    path: '/jobDetail/:job_id',
    name: 'JobDetail',
    component: JobDetail
  },
  {
    path: '/news/:newsId',
    name: 'NewsDetail',
    component: NewsDetail
  },
  {
    path: '/myApply',
    name: 'myApply',
    component: myApply
  },
  {
    path: '/epManageApply',
    name: 'epManageApply',
    component: epManageApply
  },
  {
    path: '/epPublishNews',
    name: 'epPublishNews',
    component: epPublishNews
  },
  {
    path: '/JobRelease',
    name: 'JobRelease',
    component: JobRelease
  },
  {
    path: '/ManageReleasedJob',
    name: 'ManageReleasedJob',
    component: ManageReleasedJob
  },

  {
    path: '/manageAllJobs',
    name: 'manageAllJobs',
    component: manageAllJobs
  },
  {
    path: '/manageAllnews',
    name: 'manageAllnews',
    component: manageAllnews
  },
  {
    path: '/manageAllUsers',
    name: 'manageAllUsers',
    component: manageAllUsers
  },
  {
    path: '/postAdminNews',
    name: 'postAdminNews',
    component: postAdminNews
  },
  {
    path: '/newsEp',
    name: 'newsEp',
    component: epNewsList
  }
  
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router