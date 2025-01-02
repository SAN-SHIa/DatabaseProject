import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Layout/Header';
import Footer from './components/Layout/Footer';
import Sidebar from './components/Layout/Sidebar';

import Login from './components/Auth/Login';
import Register from './components/Auth/Register';

import ResumeForm from './components/Profile/ResumeForm';
import JobPreferences from './components/Profile/JobPreferences';
import JobList from './components/Jobs/JobList';
import JobApplication from './components/Jobs/JobApplication';
import NewsList from './components/News/NewsList';

function App() {
  return (
    <Router>
      <div className="app">
        <Header />
        <div className="main-content">
          <Sidebar />
          <div className="content">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />

              <Route path="/resume" element={<ResumeForm />} />
              <Route path="/preferences" element={<JobPreferences />} />
              <Route path="/jobs" element={<JobList />} />
              <Route path="/apply/:jobId" element={<JobApplication />} />
              <Route path="/news" element={<NewsList />} />
            </Routes>
          </div>
        </div>
        <Footer />
      </div>
    </Router>
  );
}

export default App; 