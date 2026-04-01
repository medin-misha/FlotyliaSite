import axios from "axios";
import api from "./api";

function getErrorMessage(error, fallbackMessage) {
    if (axios.isAxiosError(error)) {
        const responseData = error.response?.data;
        const responseMessage =
            responseData?.message ||
            responseData?.error ||
            responseData?.detail;

        if (typeof responseMessage === "string" && responseMessage.trim()) {
            return responseMessage;
        }

        if (error.code === "ECONNABORTED") {
            return "Request timed out";
        }

        if (!error.response) {
            return "Unable to connect to server";
        }
    }

    if (error instanceof Error && error.message) {
        return error.message;
    }

    return fallbackMessage;
}

function createRequestError(error, fallbackMessage) {
    const requestError = new Error(getErrorMessage(error, fallbackMessage));

    if (axios.isAxiosError(error)) {
        requestError.status = error.response?.status;
        requestError.data = error.response?.data;
    }

    return requestError;
}

const APIPosts = {
    createPost: async (data, url) => {
        console.log(data)
        try {
            return await api.post(url, data)
        } catch (error) {
            console.error(`Failed to create resource at ${url}`, error)
            throw createRequestError(error, "Failed to create resource")
        }
    },
    createFile: async (file) => {
        try {
            const formData = new FormData()
            formData.append("file", file)

            return await api.post("/files", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
        } catch (error) {
            console.error("Failed to upload file", error)
            throw createRequestError(error, "Failed to upload file")
        }
    }
}

export default APIPosts
