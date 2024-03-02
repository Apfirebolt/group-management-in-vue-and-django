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
              <h1 class="flex-1 text-2xl font-bold text-gray-900">Photos</h1>
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

        <!-- Details sidebar -->
        <aside
          class="hidden w-96 bg-white p-8 border-l border-gray-200 overflow-y-auto lg:block"
        >
          <div class="pb-16 space-y-6">
            <div>
              <div
                class="block w-full aspect-w-10 aspect-h-7 rounded-lg overflow-hidden"
              >
                <img :src="currentFile.source" alt="" class="object-cover" />
              </div>
              <div class="mt-4 flex items-start justify-between">
                <div>
                  <h2 class="text-lg font-medium text-gray-900">
                    <span class="sr-only">Details for </span
                    >{{ currentFile.name }}
                  </h2>
                  <p class="text-sm font-medium text-gray-500">
                    {{ currentFile.size }}
                  </p>
                </div>
                <button
                  type="button"
                  class="ml-4 bg-white rounded-full h-8 w-8 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <HeartIcon class="h-6 w-6" aria-hidden="true" />
                  <span class="sr-only">Favorite</span>
                </button>
              </div>
            </div>
            <div>
              <h3 class="font-medium text-gray-900">Information</h3>
              <dl
                class="mt-2 border-t border-b border-gray-200 divide-y divide-gray-200"
              >
                <div
                  v-for="key in Object.keys(currentFile.information)"
                  :key="key"
                  class="py-3 flex justify-between text-sm font-medium"
                >
                  <dt class="text-gray-500">{{ key }}</dt>
                  <dd class="text-gray-900">
                    {{ currentFile.information[key] }}
                  </dd>
                </div>
              </dl>
            </div>
            <div>
              <h3 class="font-medium text-gray-900">Description</h3>
              <div class="mt-2 flex items-center justify-between">
                <p class="text-sm text-gray-500 italic">
                  Add a description to this image.
                </p>
                <button
                  type="button"
                  class="bg-white rounded-full h-8 w-8 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <PencilIcon class="h-5 w-5" aria-hidden="true" />
                  <span class="sr-only">Add description</span>
                </button>
              </div>
            </div>
            <div>
              <h3 class="font-medium text-gray-900">Shared with</h3>
              <ul
                role="list"
                class="mt-2 border-t border-b border-gray-200 divide-y divide-gray-200"
              >
                <li
                  v-for="person in currentFile.sharedWith"
                  :key="person.id"
                  class="py-3 flex justify-between items-center"
                >
                  <div class="flex items-center">
                    <img
                      :src="person.imageUrl"
                      alt=""
                      class="w-8 h-8 rounded-full"
                    />
                    <p class="ml-4 text-sm font-medium text-gray-900">
                      {{ person.name }}
                    </p>
                  </div>
                  <button
                    type="button"
                    class="ml-6 bg-white rounded-md text-sm font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Remove<span class="sr-only"> {{ person.name }}</span>
                  </button>
                </li>
              </ul>
            </div>
            <div class="flex">
              <button
                type="button"
                class="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Download
              </button>
              <button
                type="button"
                class="flex-1 ml-3 bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Delete
              </button>
            </div>
          </div>
        </aside>
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
const files = [
  {
    name: "IMG_4985.HEIC",
    size: "3.9 MB",
    source:
      "https://images.unsplash.com/photo-1582053433976-25c00369fc93?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80",
    current: true,
  },
  // More files...
];
const currentFile = {
  name: "IMG_4985.HEIC",
  size: "3.9 MB",
  source:
    "https://images.unsplash.com/photo-1582053433976-25c00369fc93?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=512&q=80",
  information: {
    "Uploaded by": "Marie Culver",
    Created: "June 8, 2020",
    "Last modified": "June 8, 2020",
    Dimensions: "4032 x 3024",
    Resolution: "72 x 72",
  },
  sharedWith: [
    {
      id: 1,
      name: "Aimee Douglas",
      imageUrl:
        "https://images.unsplash.com/photo-1502685104226-ee32379fefbe?ixlib=rb-=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=3&w=1024&h=1024&q=80",
    },
    {
      id: 2,
      name: "Andrea McMillan",
      imageUrl:
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&ixqx=oilqXxSqey&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80",
    },
  ],
};

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
      await group.addGroup(groupData);
      await group.getGroupsAction();
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
      files,
      currentFile,
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
