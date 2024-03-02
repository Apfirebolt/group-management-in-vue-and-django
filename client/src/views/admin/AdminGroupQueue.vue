<template>
  <div class="flex container mx-auto">
    <div class="flex-1 p-4">
      <h2 class="text-2xl text-gray-900">
        Admin Group Queues
      </h2>
    </div>
  </div>

  <GroupQueueTable
    :getGroupQueues="getGroupQueues"
  />
  
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">

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
import ConfirmModal from "../../components/ConfirmModal.vue";
import GroupQueueTable from "../../components/GroupQueueTable.vue";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
} from "@headlessui/vue";
import { onMounted, computed, ref } from "vue";
import { useGroup } from "../../store/group";

const group = useGroup();
const isConfirmOpen = ref(false);
const selectedGroup = ref(null);
const deleteConfirmMessage = ref("");

const setIsConfirmOpenFalse = () => {
  isConfirmOpen.value = false;
  deleteConfirmMessage.value = "";
};

const getGroupQueues = computed(() => {
  return group.getGroupQueues;
});

const deleteGroupUtil = async () => {
  setIsConfirmOpenFalse();
  await group.deleteGroup(selectedGroup.value.id);
  await group.getGroupQueuesAction();
};

onMounted(() => {
  group.getGroupsAction();
  group.getGroupQueuesAction();
});
</script>
