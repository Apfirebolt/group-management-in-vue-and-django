<template>
  <div class="flex container mx-auto">
      <div class="flex-1 p-4">
        <h2 class="text-2xl text-gray-900">
          Admin Users Page
        </h2>
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
          EMAIL
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          USERNAME
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          ROLE
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
      <tr v-for="user in getUsers" :key="user.id">
        <td
          class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
        >
          {{ user.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.email }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.username }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.role }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap font-medium">
          <button @click="openUserEditForm(user)" class="text-indigo-600 hover:text-indigo-900">Edit</button>
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
              <UserForm :updateUserUtil="updateUserUtil" :user="selectedUser" />
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
  </div>
</template>

<script setup>
import UserForm from '../../components/UserForm.vue';
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel
} from '@headlessui/vue'
import { onMounted, computed, ref } from "vue";
import { useUser } from "../../store/user";

const user = useUser();
const isOpen = ref(false);
const selectedUser = ref(null);

const setIsOpen = (value) => {
  isOpen.value = value;
};

const closeModal = () => {
  setIsOpen(false);
};

const openUserEditForm = (user) => {
  selectedUser.value = user;
  setIsOpen(true);
};

const getUsers = computed(() => {
  return user.getUsers;
});

const updateUserUtil = async (userData) => {
  closeModal();
  await user.updateUser(userData);
  await user.getUsersAction();
};

onMounted(() => {
  user.getUsersAction();
});
</script>
