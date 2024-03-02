import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useGroup = defineStore("item", {
  state: () => ({
    group: ref({}),
    groups: ref([]),
    groupTasks: ref([]),
    groupQueues: ref([]),
    loading: ref(false),
  }),

  getters: {
    getgroup() {
      return this.group;
    },
    getGroups() {
      return this.groups;
    },
    getGroupTasks() {
      return this.groupTasks;
    },
    getGroupQueues() {
      return this.groupQueues;
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

    async getGroupTasksAction() {
      try {
        const headers = { 
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("group-tasks", {
          headers,
        });
        this.groupTasks = response.data;
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getMyGroupTasksAction() {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("my-group-tasks", {
          headers,
        });
        this.groupTasks = response.data;
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getGroupQueuesAction() {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("group-queues", {
          headers,
        });
        this.groupQueues = response.data;
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getMyGroupQueuesAction() {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("my-group-queues", {
          headers,
        });
        this.groupQueues = response.data;
      } catch (error) {
        console.log(error);
        return error;
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