<template>
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Admin Supplier Page
      </h2>
    </div>

    <table class="table-fixed min-w-full rounded-lg shadow-md">
      <thead>
        <tr class="bg-gray-100 text-left">
          <th class="w-10 py-4 px-6">ID</th>
          <th class="w-50 py-4 px-6">Name</th>
          <th class="w-30 py-4 px-6">Description</th>
          <th class="w-30 py-4 px-6">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(supplier, index) in suppliers"
          class="border-b hover:bg-gray-200"
        >
          <td class="text-center py-4 px-6">
            {{ supplier.id }}
          </td>
          <td class="py-4 px-6">
            {{ supplier.name }}
          </td>
          <td class="py-4 px-6 truncate">
            {{ supplier.created_at }}
          </td>
          <td class="py-4 px-6">
            <span
              class="inline-flex items-center px-3 py-2 rounded-full text-white bg-green-500 font-bold"
            >
              Actions
            </span>
          </td>
        </tr>
      </tbody>
    </table>
    {{ suppliers }}
  </div>
</template>

<script setup>
import httpClient from "../../plugins/interceptor";
import { onMounted, computed, ref } from "vue";
import { useItem } from "../../store/item";

const item = useItem();
const suppliers = ref([]);

const getSuppliers = computed(() => {
  return item.getSuppliers.value;
});

console.log('None ', getSuppliers);

onMounted(() => {
  item.getSuppliersAction();  
  httpClient
    .get("/suppliers")
    .then((response) => {
      suppliers.value = response.data;
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
});
</script>
