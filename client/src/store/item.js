import { defineStore } from "pinia";
import { ref } from "vue";
import httpClient from "../plugins/interceptor";
import { useAuth } from "./auth";
import { useToast } from "vue-toastification";

const toast = useToast();
const auth = useAuth();

export const useItem = defineStore("item", {
  state: () => ({
    supplier: ref({}),
    suppliers: ref([]),
    category: ref({}),
    categories: ref([]),
    loading: ref(false),
  }),

  getters: {
    getSupplier() {
      return this.supplier;
    },
    getSuppliers() {
      return this.suppliers;
    },
    getCategory() {
      return this.category;
    },
    getCategories() {
      return this.categories;
    },
    isLoading() {
      return this.loading;
    },
  },

  actions: {
    async addSupplier(supplierData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("suppliers/create", supplierData, {
          headers,
        });
        toast.success("Supplier added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async updateSupplier(supplierData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.put(`suppliers/${supplierData.id}`, supplierData, {
          headers,
        });
        toast.success("Supplier updated!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getSupplierAction(supplierId) {
      try {
        const response = await httpClient.get("supplier/" + supplierId);
        console.log(response);
      } catch (error) {
        console.log(error);
        
      }
    },

    async getSuppliersAction(page = 1) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("suppliers?page=" + page, {
          headers,
        });
        this.suppliers = response.data;
      } catch (error) {
        console.log(error);
        return error
      }
    },

    async deleteSupplier(supplierId) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.delete("suppliers/" + supplierId, {
          headers,
        });
        toast.success("Supplier deleted!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async addCategory(categoryData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.post("categories/create", categoryData, {
          headers,
        });
        toast.success("Category added!");
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async updateCategory(categoryData) {
      try {
        const headers = {
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.put(`categories/${categoryData.id}`, categoryData, {
          headers,
        });
        if (response.status === 200) {
          toast.success("Category updated!");
        }
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    async getCategoryAction(categoryId) {
      try {
        const response = await httpClient.get("category/" + categoryId);
        console.log(response);
      } catch (error) {
        console.log(error);
      }
    },

    async getCategoriesAction(page = 1) {
      try {
        const headers = { 
          Authorization: `Bearer ${auth.authData.access}`,
        };
        const response = await httpClient.get("categories?page=" + page, {
          headers,
        });
        this.categories = response.data;
      } catch (error) {
        console.log(error);
        return error;
      }
    },

    resetData() {
      this.supplier = {};
      this.suppliers = [];
      this.category = {};
      this.categories = [];
    },
  },
});