<template>
  <p class="container bg-primary mx-auto">
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Expedita, culpa!
  </p>
  <table class="container mx-auto my-3 divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          ID
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          NAME
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          CREATED AT
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          ACTIONS
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="supplier in getSuppliers" :key="supplier.id">
        <td
          class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
        >
          {{ supplier.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ supplier.name }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ supplier.created_at }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium">
          <button @click="openSupplierEditForm(supplier)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Admin Supplier Page
      </h2>

      <button class="" @click="openSupplierAddForm">
        Add Supplier
      </button>
    </div>

    <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="closeModal" class="relative z-10">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black/25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div
          class="flex min-h-full items-center justify-center p-4 text-center"
        >
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <SupplierForm :addSupplierUtil="addSupplierUtil" :supplier="selectedSupplier" />
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
  </div>
</template>

<script setup>
import SupplierForm from '../../components/SupplierForm.vue';
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel
} from '@headlessui/vue'
import { onMounted, computed, ref } from "vue";
import { useItem } from "../../store/item";

const item = useItem();
const isOpen = ref(true);
const selectedSupplier = ref(null);

const setIsOpen = (value) => {
  isOpen.value = value;
};

const closeModal = () => {
  setIsOpen(false);
};

const openSupplierEditForm = (supplier) => {
  selectedSupplier.value = supplier;
  setIsOpen(true);
};

const getSuppliers = computed(() => {
  return item.getSuppliers;
});

const openSupplierAddForm = () => {
  selectedSupplier.value = null;
  setIsOpen(true);
};

const addSupplierUtil = async (supplierData) => {
  closeModal();
  await item.addSupplier(supplierData);
  await item.getSuppliersAction();
};


onMounted(() => {
  item.getSuppliersAction();
});
</script>
