<template>
  <main class="flex-1 mx-auto max-w-7xl overflow-y-auto">
    <div class="pt-8 px-4 sm:px-6 lg:px-8">
      <div class="flex">
        <h1 class="flex-1 text-2xl font-bold text-gray-900">Profile</h1>
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
          </div>
        </div>
      </div>

      <section class="mt-8 pb-16" aria-labelledby="gallery-heading">
        <div class="pb-16 space-y-6">
          <div>
            <div class="block rounded-lg overflow-hidden">
              <img
                :src="currentFile.source"
                alt=""
                class="object-cover w-96 h-64"
              />
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
                class="py-3 flex justify-between text-sm font-medium"
              >
                <dt class="text-gray-500">
                  Email
                </dt>
                <dd class="text-gray-900">
                  {{ userData.email }}
                </dd>
              </div>
              <div
                class="py-3 flex justify-between text-sm font-medium"
              >
                <dt class="text-gray-500">
                  Username
                </dt>
                <dd class="text-gray-900">
                  {{ userData.username }}
                </dd>
              </div>
              <div
                class="py-3 flex justify-between text-sm font-medium"
              >
                <dt class="text-gray-500">
                  Role
                </dt>
                <dd class="text-gray-900">
                  {{ userData.role }}
                </dd>
              </div>
              <div
                class="py-3 flex justify-between text-sm font-medium"
              >
                <dt class="text-gray-500">
                  Admin
                </dt>
                <dd class="text-gray-900">
                  {{ userData.is_admin ? "Yes" : "No"}}
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
      </section>
      {{ userData }}
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useUser } from "../store/user";
import { useAuth } from "../store/auth";

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

const mobileMenuOpen = ref(false);
const auth = useAuth();
const user = useUser();
const selectedTab = ref("My Tasks");
const isOpen = ref(false);

const setIsOpen = (value) => {
  isOpen.value = value;
};

const updateProfileUtil = async (payload) => {
  console.log(payload)
};

const userData = computed(() => user.user);

onMounted(() => {
  user.getUserAction(auth.authData.id)
});
</script>
