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
      <section class="mt-8 pb-16" aria-labelledby="gallery-heading">
        <div class="pb-16 space-y-6">
          <div>
            <div class="flex rounded-lg overflow-hidden">
              <img v-if="userData.profile_image && !previewImage" :src="appUrl + userData.profile_image" alt="" class="object-cover w-96 h-64 mr-2" />
              <img v-if="previewImage"
                :src="previewImage"
                class="object-cover w-96 h-64 mr-2"
              />
              
            </div>
          </div>
          <div>
            <button
              @click="onFileUploadClick"
              class="flex-1 mb-3 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Upload Photo
            </button>
            <input
              type="file"
              ref="fileInput"
              @change="fileUploadChange"
              hidden
            />

            <h3 class="font-medium text-gray-900">Information</h3>
            <dl
              class="mt-2 border-t border-b border-gray-200 divide-y divide-gray-200"
            >
              <div class="py-3 flex justify-between text-sm font-medium">
                <dt class="text-gray-500">Email</dt>
                <input
                  v-if="editMode"
                  id="email"
                  v-model="formData.email"
                  name="email"
                  type="email"
                  class="appearance-none block px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
                <dd v-else class="text-gray-900">
                  {{ userData.email }}
                </dd>
              </div>
              <div class="py-3 flex justify-between text-sm font-medium">
                <dt class="text-gray-500">Username</dt>
                <input
                  v-if="editMode"
                  id="username"
                  v-model="formData.username"
                  name="username"
                  type="text"
                  class="appearance-none block px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
                <dd v-else class="text-gray-900">
                  {{ userData.username }}
                </dd>
              </div>
              <div class="py-3 flex justify-between text-sm font-medium">
                <dt class="text-gray-500">Role</dt>
                <dd class="text-gray-900">
                  {{ userData.role }}
                </dd>
              </div>
              <div class="py-3 flex justify-between text-sm font-medium">
                <dt class="text-gray-500">Admin</dt>
                <dd class="text-gray-900">
                  {{ userData.is_admin ? "Yes" : "No" }}
                </dd>
              </div>
            </dl>
          </div>
          <button
            @click="editMode = !editMode"
            type="button"
            class="bg-white rounded-full h-8 w-8 flex items-center justify-center text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <PencilIcon class="h-5 w-5" aria-hidden="true" />
            <span class="sr-only">Add description</span>
          </button>
          <div class="flex items-center md:w-1/3">
            <button
              @click="updateProfileUtil"
              type="button"
              class="flex-1 bg-indigo-600 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Update Profile
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
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from "vue";
import { useUser } from "../store/user";
import { useAuth } from "../store/auth";
const editMode = ref(false);
const fileInput = ref(null);

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

const mobileMenuOpen = ref(false);
const auth = useAuth();
const user = useUser();
const selectedTab = ref("My Tasks");
const isOpen = ref(false);
const previewImage = ref(null);
const appUrl = import.meta.env.VITE_APP_API_URL

const setIsOpen = (value) => {
  isOpen.value = value;
};

const updateProfileUtil = async () => {
  const payload = {
    id: auth.authData.id,
    email: formData.email,
    username: formData.username,
    profile_image: formData.profile_image,
  };
  await user.updateUser(payload);
  await user.getUserAction(auth.authData.id);
};

const userData = computed(() => user.user);

const formData = reactive({
  email: "",
  username: "",
  profile_image: "",
});

watch(userData, (newVal) => {
  formData.email = newVal.email;
  formData.username = newVal.username;
});

const onFileUploadClick = () => {
  fileInput.value.click(); // Trigger the hidden file selection dialog
};

const fileUploadChange = (event) => {
  // Handle uploaded files here
  const files = event.target.files;
  console.log(files);
  formData.profile_image = files[0];

  if (files && files[0]) {
    const reader = new FileReader();

    reader.onload = (e) => {
      previewImage.value = e.target.result;
    };

    reader.readAsDataURL(files[0]);
  }
};

onMounted(() => {
  user.getUserAction(auth.authData.id);
});
</script>
