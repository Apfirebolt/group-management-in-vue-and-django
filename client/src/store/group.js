import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useItem = defineStore("item", {
  state: () => ({
    group: ref({}),
    groups: ref([]),
    loading: ref(false),
  }),

  getters: {
    getgroup() {
      return this.group;
    },
    getGroups() {
      return this.groups;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addGroup(groupData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("groups/create", groupData, {
          headers,
        });
        toast.success("Group added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async updateGroup(groupData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.put(`groups/${groupData.id}`, groupData, {
          headers,
        });
        toast.success("Group updated!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getGroupAction(groupId) {
      try {
        const response = await httpClient.get("group/" + groupId);
        console.log(response);
      } catch (error) {
        console.log(error);
        
      }
    },

    async getGroupsAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("groups?page=" + page, {
          headers,
        });
        this.groups = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async deleteGroup(groupId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.delete("groups/" + groupId, {
          headers,
        });
        toast.success("Group deleted!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetGroupData() {
      this.group = {};
      this.groups = [];
    },
  },
});