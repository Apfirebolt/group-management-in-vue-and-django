import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useUser = defineStore("user", {
  state: () => ({
    user: ref({}),
    users: ref([]),
    loading: ref(false),
  }),

  getters: {
    getUser() {
      return this.user;
    },
    getUsers() {
      return this.users;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addUser(userData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("register", userData, {
          headers,
        });
        toast.success("User added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getUserAction(userId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("users/" + userId, {
          headers,
        });
        this.user = response.data;
      } catch (error) {
        console.log(error);
        
      }
    },

    async getUsersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("users", {
          headers,
        });
        this.users = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async updateUser(userData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
          'Content-Type': 'multipart/form-data',
        };
        const response = await httpClient.put(`users/${userData.id}`, userData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("User data updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async deleteUser(userId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.delete("users/" + userId, {
          headers,
        });
        toast.success("User deleted!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetUserData() {
      this.user = {};
      this.users = [];
    },
  },
});