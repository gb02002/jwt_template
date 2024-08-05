import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:8000',
});

instance.interceptors.request.use(
    (confirg) => {
        const token = localStorage.getItem('token');
        if (token) {
            confirg.headers.Authorization = "Bearer ${token}";
        }
        return confirg;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default instance;
