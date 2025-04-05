<template>
  <div>
    <h2>Select Your Crypto and Currency</h2>
    <div class="container pt-5">
    <div class="row mb-4">
      <div class="col-md-3">
        <label for="crypto" class="form-label">Select Crypto:</label>
        <select v-model="selectedCrypto" id="crypto" class="form-select">
          <option disabled value="">Please select a cryptocurrency</option>
          <option v-for="crypto in cryptoList" :key="crypto" :value="crypto">{{ crypto }}</option>
        </select>
      </div>
      <div class="col-md-3">
        <label for="currency" class="form-label">Select Currency:</label>
        <select v-model="selectedCurrency" id="currency" class="form-select">
          <option disabled value="">Please select a currency</option>
          <option v-for="currency in currencyList" :key="currency" :value="currency">{{ currency }}</option>
        </select>
      </div>
    </div>
    <button @click="handleSubmit" class="btn btn-primary">Submit</button>
  </div>
  <div v-if="submitted" class="mt-4">
    <h4>You selected:</h4>
    <h6>Crypto: {{ selectedCrypto }}</h6>
    <h6>Currency: {{ selectedCurrency }}</h6>
    <h5>Price: $ {{ cryptoPrice }}</h5>
    <div>
      <button @click="redirectDashboard">Show past 24 hours price data</button>
    </div>
  </div>
  </div>
</template>

<script>
import { getCryptoPrices } from '../api';
export default {
  name: "HomePage",
  data() {
    return {
      selectedCrypto: "",
      selectedCurrency: "",
      cryptoPrice:"",
      cryptoList: ['Bitcoin', 'Ethereum', 'Dogecoin'],
      currencyList: ["USD", "INR", "EUR", "GBP", "CAD"],
      submitted: false,
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.selectedCrypto || !this.selectedCurrency) {
        alert("Please select both cryptocurrency and currency.");
        return;
      }
      this.submitted = true;
      const data = await getCryptoPrices(this.selectedCrypto, this.selectedCurrency);
      this.cryptoPrice = data.data
      console.log(data);
    },
    redirectDashboard() {
      this.$router.push({
      path: '/dashboard',
      query: { 
        cur: this.selectedCurrency,
        coin: this.selectedCrypto
      }
    });
  }
  }
};
</script>

<style scoped>
</style>