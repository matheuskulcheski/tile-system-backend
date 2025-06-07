import api from './api';

export const getProjects = async (filters = {}) => {
  try {
    const response = await api.get('/projects', { params: filters });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const getProject = async (id) => {
  try {
    const response = await api.get(`/projects/${id}`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const createProject = async (projectData) => {
  try {
    const response = await api.post('/projects', projectData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const updateProject = async (id, projectData) => {
  try {
    const response = await api.put(`/projects/${id}`, projectData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const deleteProject = async (id) => {
  try {
    const response = await api.delete(`/projects/${id}`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

export const getClientProjects = async (clientId) => {
  try {
    const response = await api.get(`/projects/client/${clientId}`);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : { message: 'Erro ao conectar ao servidor' };
  }
};

