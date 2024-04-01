<template>
  <div>
    <h2 class="my-4 bg-gray-100 text-center text-xl font-extrabold p-2 text-gray-900">
      {{ group ? "Update Group" : "Add Group" }}
    </h2>
    <div class="bg-white p-4 sm:rounded-lg sm:px-3">
      <form class="space-y-6" @submit="onSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Group Name
          </label>
          <div class="mt-1">
            <input id="email" v-bind="nameAttributes" v-model="name" name="name" type="text"
              placeholder="Enter User name"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" />
          </div>
          <p class="my-2 text-red-800">
            {{ errors.name }}
          </p>
        </div>

        <div>
          <label for="moderator" class="block text-sm font-medium text-gray-700">
            Group Moderators
          </label>
          <div v-if="selectedUsers.length" class="flex flex-wrap">
            <span v-for="user in selectedUsers" :key="user.id"
              class="bg-green-200 px-2 py-1 my-1 rounded-full text-green-800 mr-1">{{ user.email }}</span>
          </div>
          <p v-else class="my-2 text-red-800">
            Please select a moderator
          </p>
          <div class="mt-1">
            <Listbox v-model="moderator" multiple>
              <div class="relative mt-1">
                <ListboxButton
                  class="relative w-full cursor-default rounded-lg py-2 pl-3 text-left shadow-md focus:outline-none focus-visible:border-indigo-500 focus-visible:ring-2 focus-visible:ring-white/75 focus-visible:ring-offset-2 focus-visible:ring-offset-orange-300 sm:text-sm">

                  <div class="flex justify-between p-2">
                    <ChevronDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
                    <ListboxLabel class="block truncate">
                      Select a moderator
                    </ListboxLabel>
                  </div>
                </ListboxButton>

                <transition leave-active-class="transition duration-100 ease-in" leave-from-class="opacity-100"
                  leave-to-class="opacity-0">
                  <ListboxOptions
                    class="absolute mt-1 w-full max-h-36 overflow-x-hidden overflow-y-auto z-10 rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black/5 focus:outline-none sm:text-sm">
                    <ListboxOption v-slot="{ active, selected }" v-for="user in users" :key="user.id" :value="user.id"
                      as="template">
                      <li :class="[
        active
          ? 'bg-amber-100 text-amber-900'
          : 'text-gray-900',
        'relative cursor-default select-none py-2 pl-10 pr-4',
      ]">
                        <span :class="[
        selected ? 'font-medium' : 'font-normal',
        'block truncate',
      ]">{{ user.email }}</span>
                        <span v-if="selected" class="absolute inset-y-0 left-0 flex items-center pl-3 text-amber-600">
                          <CheckIcon class="h-5 w-5" aria-hidden="true" />
                        </span>
                      </li>
                    </ListboxOption>
                  </ListboxOptions>
                </transition>
              </div>
            </Listbox>
          </div>
          <p class="my-2 text-red-800">
            {{ errors.moderator }}
          </p>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Group Description
          </label>
          <div class="mt-1">
            <textarea name="description" id="description" cols="30" rows="6" v-model="description"
              v-bind="descriptionAttributes"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
            </textarea>
          </div>
          <p class="my-2 text-red-800">
            {{ errors.description }}
          </p>
        </div>

        <div>
          <button type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
            {{ group ? "Update Group" : "Add Group" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from "vue";
import { useForm } from "vee-validate";
import {
  Listbox,
  ListboxLabel,
  ListboxButton,
  ListboxOptions,
  ListboxOption,
} from "@headlessui/vue";
import { CheckIcon, ChevronDownIcon } from "@heroicons/vue/solid";

const props = defineProps({
  group: {
    type: Object,
    required: false,
  },
  users: {
    type: Array,
    required: true,
  },
  addGroupUtil: {
    type: Function,
    required: true,
  },
  updateGroupUtil: {
    type: Function,
    required: false,
  },
});

const moderator = ref([]);

const selectedUsers = computed(() => {
  return props.users.filter((user) => moderator.value.includes(user.id));
});

onMounted(() => {
  if (props.group) {
    name.value = props.group.name;
    description.value = props.group.description;
    moderator.value = props.group.moderator;
  }
});

// Validation, or use `yup` or `zod`
function required(value) {
  return value ? true : "This field is required";
}

// Create the form
const { defineField, handleSubmit, errors } = useForm({
  validationSchema: {
    name: required,
    description: required,
  },
});

// Define fields
const [name, nameAttributes] = defineField("name", {
  type: "text", // Initial type
  name: "name", // Initial name
});

const [description, descriptionAttributes] = defineField("description", {
  type: "text", // Initial type
  name: "description", // Initial name
});

// Submit handler
const onSubmit = handleSubmit(async (values) => {
  // add moderator to values
  if (props.group) {
    await props.updateGroupUtil({ ...payload, id: props.group.id });
    return;
  }
  const payload = { ...values, moderator: moderator.value };
  await props.addGroupUtil(payload);
});
</script>
