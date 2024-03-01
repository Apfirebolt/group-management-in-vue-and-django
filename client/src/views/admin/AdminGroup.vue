<template>
  <div class="flex container mx-auto">
    <div class="flex-1 p-4">
      <h2 class="text-2xl text-gray-900">
        Admin Groups Page
      </h2>
    </div>
    <div class="flex-1 text-right py-2">
      <button
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        @click="openGroupAddForm"
      >
        Add Group
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
          DESCRIPTION
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
      <tr v-for="group in getGroups" :key="group.id">
        <td
          class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
        >
          {{ group.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ group.name }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ group.description }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ group.created_at }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap font-medium">
          <button
            @click="openGroupEditForm(group)"
            class="bg-blue-500 hover:bg-blue-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
          >
            Edit
          </button>
          <button
            @click="setIsConfirmOpen(group)"
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
                <GroupForm
                  :users="getUsers"
                  :addGroupUtil="addGroupUtil"
                  :updateGroupUtil="updateGroupUtil"
                  :group="selectedGroup"
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
                  :confirmAction="deleteGroupUtil"
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
import GroupForm from "../../components/GroupForm.vue";
import ConfirmModal from "../../components/ConfirmModal.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import { onMounted, computed, ref } from "vue";
import { useGroup } from "../../store/group";
import { useUser } from "../../store/user";

const group = useGroup();
const user = useUser();
const isOpen = ref(false);
const isConfirmOpen = ref(false);
const selectedGroup = ref(null);
const deleteConfirmMessage = ref("");

const setIsOpen = (value) => {
  isOpen.value = value;
};

const setIsConfirmOpen = (group) => {
  isConfirmOpen.value = true;
  selectedGroup.value = group;
  deleteConfirmMessage.value = `Are you sure you want to delete ${group.name}?`;
};

const openGroupAddForm = () => {
  selectedGroup.value = null;
  setIsOpen(true);
};

const setIsConfirmOpenFalse = () => {
  isConfirmOpen.value = false;
  deleteConfirmMessage.value = "";
};

const closeModal = () => {
  setIsOpen(false);
};

const openGroupEditForm = (group) => {
  selectedGroup.value = group;
  setIsOpen(true);
};

const getGroups = computed(() => {
  return group.getGroups;
});

const getUsers = computed(() => {
  return user.getUsers;
});

const addGroupUtil = async (groupData) => {
  closeModal();
  await group.addGroup(groupData);
  await group.getGroupsAction();
};

const updateGroupUtil = async (groupData) => {
  closeModal();
  await group.updateGroup(groupData);
  await group.getGroupsAction();
};

const deleteGroupUtil = async () => {
  setIsConfirmOpenFalse();
  await group.deleteGroup(selectedGroup.value.id);
  await group.getGroupsAction();
};

onMounted(() => {
  group.getGroupsAction();
  user.getUsersAction();
});
</script>
