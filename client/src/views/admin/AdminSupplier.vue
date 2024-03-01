<template>
  <div class="flex container mx-auto">
    <div class="flex-1 p-4">
      <h2 class="text-2xl text-gray-900">
        Admin Supplier Page
      </h2>
    </div>
    <div class="flex-1 text-right py-2">
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        @click="openSupplierAddForm"
      >
        Add Supplier
      </button>
    </div>
  </div>

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
        <td class="px-6 py-4 whitespace-nowrap font-medium">
          <button
            @click="openSupplierEditForm(supplier)"
            class="bg-blue-500 hover:bg-blue-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
          >
            Edit
          </button>
          <button
            @click="setIsConfirmOpen(supplier)"
            class="bg-red-500 hover:bg-red-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
          >
            Delete
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
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
                <SupplierForm
                  :addSupplierUtil="addSupplierUtil"
                  :updateSupplierUtil="updateSupplierUtil"
                  :supplier="selectedSupplier"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>

    <TransitionRoot appear :show="isConfirmOpen" as="template">
      <Dialog as="div" @close="setIsConfirmOpenFalse" class="relative z-10">
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
                <ConfirmModal
                  :message="deleteConfirmMessage"
                  :confirmAction="deleteSupplierUtil"
                  :cancelAction="setIsConfirmOpenFalse"
                />
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import SupplierForm from "../../components/SupplierForm.vue";
import ConfirmModal from "../../components/ConfirmModal.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import { onMounted, computed, ref } from "vue";
import { useItem } from "../../store/item";

const item = useItem();
const isOpen = ref(false);
const isConfirmOpen = ref(false);
const selectedSupplier = ref(null);
const deleteConfirmMessage = ref("");

const setIsOpen = (value) => {
  isOpen.value = value;
};

const setIsConfirmOpen = (supplier) => {
  isConfirmOpen.value = true;
  selectedSupplier.value = supplier;
  deleteConfirmMessage.value = `Are you sure you want to delete ${supplier.name}?`;
};

const setIsConfirmOpenFalse = () => {
  isConfirmOpen.value = false;
  deleteConfirmMessage.value = "";
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

const updateSupplierUtil = async (supplierData) => {
  closeModal();
  await item.updateSupplier(supplierData);
  await item.getSuppliersAction();
};

const deleteSupplierUtil = async () => {
  setIsConfirmOpenFalse();
  await item.deleteSupplier(selectedSupplier.value.id);
  await item.getSuppliersAction();
};

onMounted(() => {
  item.getSuppliersAction();
});
</script>
