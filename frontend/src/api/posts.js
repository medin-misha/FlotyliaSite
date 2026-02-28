import api from "./api";

const APIPosts = {
    createPost: async (data, url) => {
        return await api.post(url, data)
    },
    createFile: async (file) => {
        const formData = new FormData()
        formData.append("file", file)
        return await api.post("/files", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
    }
}

export default APIPosts
