import { createStore } from 'vuex';
import { CRYPTO_DATA } from './constants'; 

export default createStore({
  state: {
    [CRYPTO_DATA]: null, 
    isLoading: false,
    error: null,
  },
  mutations: {
    setCryptoData(state, data) {
      state[CRYPTO_DATA] = data; 
    },
    setLoading(state, status) {
      state.isLoading = status;
    },
    setError(state, error) {
      state.error = error;
    },
  },
  getters: {
    cryptoData: (state) => state[CRYPTO_DATA],
    isLoading: (state) => state.isLoading,
    error: (state) => state.error,
  },
});