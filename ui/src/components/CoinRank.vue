<template>
  <div class="coin-table">
    <div class="pb-4">
      <h2>Coin Volatility Ranks (With Past 24 Hours Data)</h2>
    </div>
    <div class="pb-4" v-if="$route.query.coin">
      <button class="btn btn-primary" @click="refreshDashboard">Get Volatility Ranks for Collected Coins</button>
    </div>
    <table class="table">
      <thead>
        <tr>
          <th @click="sortBy('key')">Coin {{ sortIcon('key') }}</th>
          <th @click="sortBy('deviation')">Deviation {{ sortIcon('deviation') }}</th>
          <th @click="sortBy('rank')">Rank {{ sortIcon('rank') }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="coin in sortedCoins" :key="coin.id">
          <td>{{ coin.key }}</td>
          <td>{{ coin.deviation }}</td>
          <td>{{ coin.rank }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {  getCoinRank } from '../api';

export default {
  name: 'CoinRank',
  data() {
    return {
      coins: [],
      sortKey: 'rank',
      sortOrder: 'asc'
    }
  },
  computed: {
    sortedCoins() {
      return [...this.coins].sort((a, b) => {
        const modifier = this.sortOrder === 'asc' ? 1 : -1
        return a[this.sortKey] > b[this.sortKey] ? modifier : -modifier
      })
    }
  },
  methods: {
     /* eslint-disable */ 
    async fetchCoinData(coin, cur) {
      try {
        let coinValue = coin ? coin : this.$route.query.coin;
        let curValue = cur ? cur : this.$route.query.cur;
        const response = await getCoinRank(coinValue, curValue);
        console.log(' #Response ', response)
        this.coins = response.data.map(coin => ({
          id: coin.id,
          key: coin.key.toUpperCase(),
          deviation: coin.std_deviation,
          rank: coin.rank
        }))
      } catch (error) {
        console.error('Error fetching data:', error)
      }
    },
    sortBy(key) {
      if (this.sortKey === key) {
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortKey = key
        this.sortOrder = 'asc'
      }
    },
    sortIcon(key) {
      if (this.sortKey !== key) return ''
      return this.sortOrder === 'asc' ? '↑' : '↓'
    },
    refreshDashboard() {
      this.$route.query.coin = '';
      this.$route.query.cur='';
      this.fetchCoinData();
  },
  },
  mounted() {
    this.fetchCoinData()
  }
}
</script>

<style scoped>
.coin-table {
  margin: 20px;
}
.table {
  width: 100%;
  border-collapse: collapse;
  font-family: Arial, sans-serif;
}
th {
  background-color: #f8f9fa;
  cursor: pointer;
  padding: 12px;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
}
td {
  padding: 10px 12px;
  border-bottom: 1px solid #dee2e6;
}
th:hover {
  background-color: #e9ecef;
}
</style>