import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    headers: {
        "Content-Type": "application/json",
    }, 
    timeout: 10000,
    timeoutErrorMessage: "Request timed out",
})

api.interceptors.request.use(
    (config) => {
        return config
    },
    (error) => {
        console.log(error)  
        return Promise.reject(error)
    }
)

export default api