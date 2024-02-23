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
    loading: ref(false),
  }),

  getters: {
    getSupplier() {
      return this.supplier;
    },
    getSuppliers() {
      return this.suppliers;
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
        const response = await httpClient.post("suppliers", supplierData, {
          headers,
        });
        toast.success("Supplier added!");
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
        console.log('Supplier data', this.suppliers);
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

    resetSupplierData() {
      this.supplier = {};
      this.suppliers = [];
    },
  },
});