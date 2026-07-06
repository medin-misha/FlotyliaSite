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

function getErrorType(error, action) {
    if (axios.isAxiosError(error)) {
        if (error.code === "ECONNABORTED") {
            return "timeout";
        }

        if (!error.response) {
            return "network";
        }

        const status = error.response.status;

        if (status === 503) {
            return "service_unavailable";
        }

        if (status >= 500) {
            return "server";
        }

        if (status === 400 || status === 422) {
            return "validation";
        }
    }

    if (action === "upload") {
        return "upload";
    }

    return "unknown";
}

function createRequestError(error, fallbackMessage, action = "request") {
    const requestError = new Error(getErrorMessage(error, fallbackMessage));

    if (axios.isAxiosError(error)) {
        requestError.status = error.response?.status;
        requestError.data = error.response?.data;
    }

    requestError.type = getErrorType(error, action);
    requestError.action = action;

    return requestError;
}

const APIPosts = {
    registerUser: async (payload, file1, file2, file1_desc, file2_desc) => {
        try {
            const formData = new FormData()
            formData.append("user_data", JSON.stringify(payload))
            formData.append("file1", file1)
            formData.append("file2", file2)
            if (file1_desc) formData.append("file1_description", file1_desc)
            if (file2_desc) formData.append("file2_description", file2_desc)

            return await api.post("/users/register", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
                timeout: 120000,
            })
        } catch (error) {
            console.error("Failed to register user atomically", error)
            throw createRequestError(error, "Failed to register user", "upload")
        }
    }
}

export default APIPosts
