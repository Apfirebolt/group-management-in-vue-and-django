<template>
    <div class="h-full flex">
      <!-- Content area -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- <v-stage :config="configKonva">
          <v-layer>
            <v-circle :config="configCircle"></v-circle>
          </v-layer>
        </v-stage> -->
        <!-- Main content -->
        <div class="flex-1 flex items-stretch overflow-hidden">
          <main class="flex-1 overflow-y-auto">
            <div class="pt-8 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div class="flex">
                <h1 class="flex-1 text-2xl font-bold">My Dashboard</h1>
                <div
                  class="ml-6 bg-gray-100 p-0.5 rounded-lg flex items-center sm:hidden"
                >
                  <button
                    type="button"
                    class="p-1.5 rounded-md text-gray-400 hover:bg-white hover:shadow-sm focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                  >
                    <ViewListIcon class="h-5 w-5" aria-hidden="true" />
                    <span class="sr-only">Use list view</span>
                  </button>
                  <button
                    type="button"
                    class="ml-0.5 bg-white p-1.5 rounded-md shadow-sm text-gray-400 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                  >
                    <ViewGridIconSolid class="h-5 w-5" aria-hidden="true" />
                    <span class="sr-only">Use grid view</span>
                  </button>
                </div>
              </div>
  
              <!-- Tabs -->
              <div class="mt-3 sm:mt-2">
                <div class="sm:hidden">
                  <label for="tabs" class="sr-only">Select a tab</label>
                  <!-- Use an "onChange" listener to redirect the user to the selected tab URL. -->
                  <select
                    id="tabs"
                    name="tabs"
                    class="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                  >
                    <option selected="">Recently Viewed</option>
                    <option>Recently Added</option>
                    <option>Favorited</option>
                  </select>
                </div>
                <div class="hidden sm:block">
                  <div class="flex items-center border-b border-gray-200">
                    <nav
                      class="flex-1 -mb-px flex space-x-6 xl:space-x-8"
                      aria-label="Tabs"
                    >
                      <span
                        v-for="tab in tabs"
                        :key="tab.name"
                        @click="selectedTab = tab.name"
                        :aria-current="tab.current ? 'page' : undefined"
                        :class="[
                          selectedTab === tab.name
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 cursor-pointer',
                        ]"
                      >
                        {{ tab.name }}
                      </span>
                    </nav>
                    <button
                      class="bg-blue-500 mb-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      @click="openGroupAddForm"
                    >
                      Add Group
                    </button>
                  </div>
                </div>
              </div>
  
              <section class="mt-8 pb-16" aria-labelledby="gallery-heading">
                <TaskTable
                  v-if="selectedTab === 'My Tasks'"
                  :getGroupTasks="myGroupTasks"
                  :approveTask="approveTaskUtil"
                  :dashboard-view="true"
                />
                <GroupQueueTable
                  v-if="selectedTab === 'My Groups'"
                  :getGroupQueues="myGroupQueues"
                />
              </section>
            </div>
          </main>
        </div>
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
                  class="w-full max-w-lg transform overflow-hidden bg-white p-6 text-left align-middle shadow-xl transition-all"
                >
                  <GroupForm :users="getUsers" :addGroupUtil="addGroupUtil" />
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </TransitionRoot>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from "vue";
  import { useGroup } from "../store/group";
  import { useUser } from "../store/user";
  import GroupQueueTable from "../components/GroupQueueTable.vue";
  import TaskTable from "../components/TaskTable.vue";
  import GroupForm from "../components/GroupForm.vue";
  
  import {
    Dialog,
    DialogPanel,
    DialogOverlay,
    Menu,
    MenuButton,
    MenuItem,
    MenuItems,
    TransitionChild,
    TransitionRoot,
  } from "@headlessui/vue";
  import {
    CogIcon,
    CollectionIcon,
    HeartIcon,
    HomeIcon,
    MenuAlt2Icon,
    PhotographIcon,
    PlusSmIcon as PlusSmIconOutline,
    UserGroupIcon,
    ViewGridIcon as ViewGridIconOutline,
    XIcon,
  } from "@heroicons/vue/outline";
  import {
    PencilIcon,
    PlusSmIcon as PlusSmIconSolid,
    SearchIcon,
    ViewGridIcon as ViewGridIconSolid,
    ViewListIcon,
  } from "@heroicons/vue/solid";
  
  const userNavigation = [
    { name: "Your profile", href: "#" },
    { name: "Sign out", href: "#" },
  ];
  const tabs = [
    { name: "My Tasks", current: true },
    { name: "My Groups", current: false },
  ];
  
  export default {
    components: {
      Dialog,
      DialogOverlay,
      Menu,
      MenuButton,
      MenuItem,
      MenuItems,
      TransitionChild,
      TransitionRoot,
      HeartIcon,
      MenuAlt2Icon,
      PencilIcon,
      PlusSmIconOutline,
      PlusSmIconSolid,
      SearchIcon,
      ViewGridIconSolid,
      ViewListIcon,
      XIcon,
      GroupQueueTable,
      TaskTable,
      GroupForm,
      DialogPanel,
    },
    setup() {
      const mobileMenuOpen = ref(false);
      const group = useGroup();
      const user = useUser();
      const selectedTab = ref("My Tasks");
      const isOpen = ref(false);
  
      const setIsOpen = (value) => {
        isOpen.value = value;
      };
  
      const myGroupTasks = computed(() => {
        return group.getGroupTasks;
      });
  
      const myGroupQueues = computed(() => {
        return group.getGroupQueues;
      });
  
      const getGroups = computed(() => {
        return group.getGroups;
      });
  
      const getUsers = computed(() => {
        return user.getUsers;
      });
  
      const approveTaskUtil = async (payload) => {
        await group.approveTask(payload);
        await group.getMyGroupTasksAction();
      };
  
      const openGroupAddForm = () => {
        setIsOpen(true);
      };
  
      const closeModal = () => {
        setIsOpen(false);
      };
  
      const addGroupUtil = async (groupData) => {
        closeModal();
        console.log(groupData);
        await group.addGroup(groupData);
        await group.getMyGroupQueuesAction();
      };
  
      onMounted(() => {
        group.getMyGroupQueuesAction();
        group.getMyGroupTasksAction();
        group.getGroupsAction();
        user.getUsersAction();
      });
  
      return {
        userNavigation,
        tabs,
        mobileMenuOpen,
        myGroupQueues,
        myGroupTasks,
        selectedTab,
        approveTaskUtil,
        getGroups,
        getUsers,
        isOpen,
        openGroupAddForm,
        addGroupUtil,
        closeModal,
      };
    },
  };
  </script>
  
  <style lang="scss">
  
  main {
    h1 {
      color: $primaryColor;
    }
  }
  
  </style>
  