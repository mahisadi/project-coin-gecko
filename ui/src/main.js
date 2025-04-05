import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'chartjs-adapter-date-fns';  // Import the date adapter
import { Chart as ChartJS } from 'chart.js';
import { Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale, TimeScale } from 'chart.js';
import 'chartjs-adapter-date-fns';  // Add the date adapter

// Register the necessary components
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,   // Register the PointElement (needed for the "point" element)
  CategoryScale,
  LinearScale,
  TimeScale
);

createApp(App)
  .use(router)
  .use(store) 
  .mount('#app');