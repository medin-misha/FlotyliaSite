import axios from "axios";
import api from "./api";

function withTrailingSlash(url) {
    return url.endsWith("/") ? url : `${url}/`
}

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
    createPost: async (data, url) => {
        try {
            return await api.post(withTrailingSlash(url), data)
        } catch (error) {
            console.error(`Failed to create resource at ${url}`, error)
            throw createRequestError(error, "Failed to create resource", "request")
        }
    },
    createFile: async (file) => {
        try {
            const formData = new FormData()
            formData.append("file", file)

            return await api.post(withTrailingSlash("/files"), formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            })
        } catch (error) {
            console.error("Failed to upload file", error)
            throw createRequestError(error, "Failed to upload file", "upload")
        }
    }
}

export default APIPosts
