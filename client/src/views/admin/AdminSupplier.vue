<template>
  <p class="container bg-primary mx-auto">
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Expedita, culpa!
  </p>
  <table class="container mx-auto my-3 divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ID
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          NAME
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          CREATED AT
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ACTIONS
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="supplier in getSuppliers" :key="supplier.id">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
          {{ supplier.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ supplier.name }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ supplier.created_at }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
          <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Admin Supplier Page
      </h2>
    </div>

  </div>
</template>

<script setup>
import httpClient from "../../plugins/interceptor";
import { onMounted, computed, ref } from "vue";
import { useItem } from "../../store/item";

const item = useItem();

const getSuppliers = computed(() => {
  return item.getSuppliers;
});

onMounted(() => {
  item.getSuppliersAction();
});
</script>
