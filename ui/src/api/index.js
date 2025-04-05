import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://tconvc8rh9.execute-api.us-east-1.amazonaws.com/dev/coin',
  timeout: 60000
});

export const getCryptoPrices = async (crypto, currency) => {
  try {
    const response = await apiClient.get(`/price?coin=${crypto}&cur=${currency}`);
    console.log("response ", response)
    return response.data;
  } catch (error) {
    console.error('Error fetching crypto prices:', error);
    throw error;
  }
};


export const fetchDataSet = async (crypto, currency) => {
  try {
    let resoure_path = '/dataset';
    if (crypto && currency){
      resoure_path = `/dataset?coin=${crypto}&cur=${currency}`
    }
    console.log(' # resoure_path ', resoure_path)
    const response = await apiClient.get(resoure_path);
    return response.data;
  } catch (error) {
    console.error('Error fetching crypto data sets:', error);
    throw error;
  }
};

export const getCoinRank = async (crypto, currency) => {
  try {
    const response = await apiClient.get(`/rank?coin=${crypto}&cur=${currency}`);
    return response.data;
  } catch (error) {
    console.error('Error getting crypto rank:', error);
    throw error;
  }
};