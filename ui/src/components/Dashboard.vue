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
import { fetchDataSet } from '../api';


ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, TimeScale);

export default {
  name: 'DashboardPage',
  components: {
    Line
  },
  data() {
    return {
      selectedCrypto: '',  
      selectedCurrency: '',  
      chartData: null, 
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
              text: 'Time'
            }
          },
          y: {
            beginAtZero: false,
            ticks: {
              stepSize: 500,
            },
            title: {
              display: true,
              text: 'Currency'
            }
          }
        }
      }
    };
  },
  mounted() {
    this.fetchChartData();
  },
  methods: {
    async fetchChartData() {
      try {
        const priceData = await fetchDataSet(this.$route.query.coin, this.$route.query.cur);
        this.processResponse(priceData);
      } catch (error) {
        console.error("Error fetching chart data:", error);
      }
    },
    processResponse(priceData){
      this.chartData = {
          datasets: Object.values(priceData.data).map(coin => ({
            label: coin.label.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
            data: coin.data,
            fill: false,
            borderColor: coin.borderColor,
            tension: 0.1
          }))
        };
    }
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
