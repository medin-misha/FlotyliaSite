import { defineStore } from "pinia";
import { useMediaQuery } from "@vueuse/core";

export const useUiStore = defineStore("ui", {
    state: () => ({
        isMobile: useMediaQuery("(max-width: 768px)"),
    }),
});