import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import "./style.css";
import router from "./routes";
import App from "./App.vue";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

// Import translations
import en from "./locales/en.json";
import de from "./locales/de.json";

const messages = {
    en: en,
    de: de,
};

const i18n = createI18n({
  legacy: false,  
  locale: 'de', // Set default locale
  fallbackLocale: "de", // Fallback to English if translation not found
  messages,
});

const app = createApp(App);
app.use(router);
app.use(createPinia());
app.use(i18n);
app.mount("#app");

const options = {
  transition: "Vue-Toastification__bounce",
  maxToasts: 20,
  newestOnTop: true,
  position: "top-right",
  timeout: 5000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: "button",
  icon: true,
  rtl: false,
};

app.use(Toast, options);
