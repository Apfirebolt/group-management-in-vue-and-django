<template>
    <div class="flex container mx-auto">
      <div class="flex-1 p-4">
        <h2 class="text-2xl text-gray-900">
          Admin Category Page
        </h2>
      </div>
      <div class="flex-1 text-right py-2">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          @click="openCategoryAddForm"
        >
          Add Category
        </button>
      </div>
    </div>
  
    <table v-if="getCategories.length" class="container mx-auto my-3 divide-y divide-gray-200">
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
        <tr v-for="category in getCategories" :key="category.id">
          <td
            class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
          >
            {{ category.id }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ category.name }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {{ formatDate(category.created_at) }}
          </td>
          <td class="px-6 py-4 whitespace-nowrap font-medium">
            <button
              @click="openCategoryEditForm(category)"
              class="bg-blue-500 hover:bg-blue-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
            >
              Edit
            </button>
            <button
              @click="setIsConfirmOpen(category)"
              class="bg-red-500 hover:bg-red-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else class="container mx-auto my-3">
      <p class="text-center text-gray-500">No categories found</p>
    </div>
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
                  <CategoryForm
                    :addCategoryUtil="addCategoryUtil"
                    :updateCategoryUtil="updateCategoryUtil"
                    :category="selectedCategory"
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
              class="flex min-h-full items-center justify-center text-center"
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
                  class="w-full max-w-md transform overflow-hidden bg-white p-2 text-left align-middle shadow-xl transition-all"
                >
                  <ConfirmModal
                    :message="deleteConfirmMessage"
                    :confirmAction="deleteCategoryUtil"
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
  import dayjs from "dayjs";
  import CategoryForm from "../../components/CategoryForm.vue";
  import ConfirmModal from "../../components/ConfirmModal.vue";
  import {
    TransitionRoot,
    TransitionChild,
    Dialog,
    DialogPanel,
  } from "@headlessui/vue";
  import { onMounted, computed, ref } from "vue";
  import { useItem } from "../../store/item";
  import { useUser } from "../../store/user";
  
  const item = useItem();
  const user = useUser();
  const isOpen = ref(false);
  const isConfirmOpen = ref(false);
  const selectedCategory = ref(null);
  const deleteConfirmMessage = ref("");
  
  const setIsOpen = (value) => {
    isOpen.value = value;
  };
  
  const setIsConfirmOpen = (category) => {
    isConfirmOpen.value = true;
    selectedCategory.value = category;
    deleteConfirmMessage.value = `Are you sure you want to delete ${category.name}?`;
  };
  
  const openCategoryAddForm = () => {
    selectedCategory.value = null;
    setIsOpen(true);
  };
  
  const setIsConfirmOpenFalse = () => {
    isConfirmOpen.value = false;
    deleteConfirmMessage.value = "";
  };
  
  const closeModal = () => {
    setIsOpen(false);
  };
  
  const openCategoryEditForm = (category) => {
    selectedCategory.value = category;
    setIsOpen(true);
  };
  
  const getCategories = computed(() => {
    return item.getCategories;
  });
  
  const addCategoryUtil = async (categoryData) => {
    closeModal();
    await item.addCategory(categoryData);
    await item.getCategoriesAction();
  };
  
  const updateCategoryUtil = async (categoryData) => {
    closeModal();
    await item.updateCategory(categoryData);
    await item.getCategoriesAction();
  };
  
  const deleteCategoryUtil = async () => {
    setIsConfirmOpenFalse();
    await item.deleteCategory(selectedCategory.value.id);
    await item.getCategoriesAction();
  };
  
  const formatDate = (date) => {
    return dayjs(date).format("YYYY-MM-DD");
  };
  
  onMounted(() => {
    item.getCategoriesAction();
  });
  </script>
  
  