import { defineStore } from "pinia";

export const useLocaleStore = defineStore("locale", {
    state: () => ({
        locale: localStorage.getItem("locale") || "en",
    }),
    actions: {
        setLocale(locale) {
            this.locale = locale;
            localStorage.setItem("locale", locale);
        },
    },
});