import api from './api';

export const getClients = async (filters = {}) => {
  try {
    const response = await api.get('/clients', { params: filters });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const getClient = async (id) => {
  try {
    const response = await api.get(`/clients/${id}`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const createClient = async (clientData) => {
  try {
    const response = await api.post('/clients', clientData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const updateClient = async (id, clientData) => {
  try {
    const response = await api.put(`/clients/${id}`, clientData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const deleteClient = async (id) => {
  try {
    const response = await api.delete(`/clients/${id}`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

