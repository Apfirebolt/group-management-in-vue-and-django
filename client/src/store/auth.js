import { defineStore } from "pinia";
import { ref } from "vue";
import router from "../routes";
import httpClient from "../plugins/interceptor";
import { useToast } from "vue-toastification";

const toast = useToast();

export const useAuth = defineStore("auth", {
  state: () => ({
    authData: JSON.parse(localStorage.getItem("user")) || null,
    users: ref([]),
    loading: ref(false),
  }),

  getters: {
    getAuthData() {
      return this.authData;
    },
    getUsers() {
      return this.users;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    logout() {
      this.authData = null;
      localStorage.removeItem("user");
      router.push("/login");
      toast.success("Logout successful!");
    },

    async loginAction(loginData) {
      try {
        const response = await httpClient
          .post("login", loginData)
          .then((response) => {
            this.authData = response.data;
            toast.success("Login successful!");
            localStorage.setItem("user", JSON.stringify(response.data));
            router.push("/dashboard");
          });
      } catch (error) {
        console.log("Inside console error", error);
        return error;
      }
    },

    async refreshToken() {
      try {
        const response = await httpClient.post("refresh", {
          refresh: this.authData.refresh,
        })
        .then((response) => {
          if (response.status === 401) {
            toast.error("Token expired,logging you out! Please login again");
            this.logout();
          }
          // console.log('Refresh token successful!', response.data);
          this.authData.access = response.data.access;
          // set the localStorage access token
          localStorage.setItem("user", JSON.stringify(this.authData));
        })
        .catch((error) => {
          console.log("Error refreshing token", error);
          this.logout();
        });
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async registerAction(registerData) {
      try {
        const response = await httpClient.post("register", registerData);
        if (response.data) {
          this.authData = response.data;
          toast.success("Registration successful!");
          localStorage.setItem("user", JSON.stringify(response.data));
          router.push("/dashboard");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getProfileData() {
      try {
        const headers = {
          Authorization: `Bearer ${this.authData.access}`,
        };
        const response = await httpClient.get("auth/profile", { headers });
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getUsersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${this.authData.access}`,
        };
        const response = await httpClient.get("users", {
          headers,
        });
        this.users = response.data;
        console.log("User data now inside auth", this.users[0].username);
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetAuth() {
      this.authData = {};
    },
  },
});
