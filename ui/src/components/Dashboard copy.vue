<template>
  <div>
    <h2>Crypto Dashboard</h2>
    <div v-if="chartData">
      <Line :data="chartData" :options="chartOptions" />
    </div>
    <div v-else>
      <p>Loading chart data...</p>
    </div>
  </div>
</template>

<script>
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, TimeScale } from 'chart.js';
ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, TimeScale);

export default {
  name: 'DashboardPageCopy',
  components: {
    Line 
  },
  data() {
    return {
      selectedCrypto: 'bitcoin',
      selectedCurrency: 'usd',
      chartData: {
        datasets: [
          {
            label: 'Bitcoin Price (USD)',
            data: [
              { x: '2025-04-01T10:00:00', y: 500 },
              { x: '2025-04-01T11:00:00', y: 1000 },
              { x: '2025-04-01T12:00:00', y: 1500 },
              { x: '2025-04-01T13:00:00', y: 2000 },
              { x: '2025-04-01T14:00:00', y: 2500 },
              { x: '2025-04-01T15:00:00', y: 3000 },
              { x: '2025-04-01T16:00:00', y: 3500 },
              { x: '2025-04-01T17:00:00', y: 4000 },
              { x: '2025-04-01T18:00:00', y: 4500 },
              { x: '2025-04-01T19:00:00', y: 5000 },
            ],
            fill: false,
            borderColor: '#42A5F5',
            tension: 0.1
          }
        ]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'hour',
              tooltipFormat: 'll HH:mm'
            },
            title: {
              display: true,
              text: 'DateTime'
            }
          },
          y: {
            beginAtZero: false,
            ticks: {
              stepSize: 500,
            },
            title: {
              display: true,
              text: 'Currency in USD'
            }
          }
        }
      }
    };
  }
};
</script>

<style scoped>
h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2rem;
}

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
</style>

