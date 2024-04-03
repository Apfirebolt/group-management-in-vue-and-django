import { createApp } from "vue";
import { createPinia } from "pinia";
import { createI18n } from "vue-i18n";
import "./style.css";
import router from "./routes";
import App from "./App.vue";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";

// import messages from './locales';

const messages = {
  en: {
    welcome: "Welcome!",
    home: "Home",
    about: "About",
  },

  de: {
    welcome: "Willkommen!",
    home: "Startseite",
    about: "Über uns",
  },
};

const i18n = createI18n({
  locale: window.navigator.language || "en", // Set default locale
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
