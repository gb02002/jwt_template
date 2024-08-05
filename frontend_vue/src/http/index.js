import axios from "axios";
import store from "@/store";
export const BASE_API_URL = "http://127.0.0.1:8000";

const $api = axios.create({
    withCredentials: true,
    baseURL: BASE_API_URL,
})

$api.interceptors.request.use(config => {
    config.headers.Authorization = 'Bearer ' + localStorage.getItem("token");
    return config
})


$api.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;

        // Проверка на статус 401
        if (error.response.status === 401) {
            try {
                await store.dispatch('refreshToken');
                const token = localStorage.getItem('token');
                if (token) {
                    originalRequest.headers.Authorization = `Bearer ${token}`;
                }
                return $api(originalRequest); // Повторный запрос с новым токеном
            } catch (refreshError) {
                console.error("Refresh token failed", refreshError);
                await store.dispatch('logout');
                router.push('/login'); // Перенаправление на страницу логина при неудаче
                return Promise.reject(refreshError); // Отклонение с ошибкой обновления
            }
        }

        return Promise.reject(error); // Отклонение с исходной ошибкой
    }
);

export default $api;
