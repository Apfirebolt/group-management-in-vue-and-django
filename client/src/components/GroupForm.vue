<template>
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white p-4 sm:rounded-lg sm:px-10">
      
      <h2 class="my-4 text-center text-xl font-extrabold text-gray-900">
        {{ group ? "Update Group" : "Add Group" }}
      </h2>
      <form class="space-y-6" @submit="onSubmit">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Group Name
          </label>
          <div class="mt-1">
            <input
              id="email"
              v-bind="nameAttributes"
              v-model="name"
              name="name"
              type="text"
              placeholder="Enter User name"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
          <p class="my-2 text-red-800">
            {{ errors.name }}
          </p>
        </div>

        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">
            Group Description
          </label>
          <div class="mt-1">
            <textarea
              name="description"
              id="description"
              cols="30"
              rows="10"
              v-model="description"
              v-bind="descriptionAttributes"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            >
            </textarea>
          </div>
          <p class="my-2 text-red-800">
            {{ errors.description }}
          </p>
        </div>

        <div>
          <label
            for="moderators"
            class="block text-sm font-medium text-gray-700"
          >
            Group Moderators
          </label>
          <div class="mt-1">
            <select
              name="moderators"
              id="moderators"
              v-bind="moderatorsAttributes"
              v-model="moderators"
              class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              multiple
            >
              <option v-for="user in users" :key="user.id" :value="user.id">
                {{ user.email }}
              </option>
            </select>
          </div>
          <p class="my-2 text-red-800">
            {{ errors.moderators }}
          </p>
        </div>

        <div>
          <button
            type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {{ group ? "Update Group" : "Add Group" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useForm } from "vee-validate";

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
    required: true,
  },
});

onMounted(() => {
  if (props.group) {
    name.value = props.group.name;
    description.value = props.group.description;
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
    moderators: required,
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

const [moderators, moderatorsAttributes] = defineField("moderators", {
  type: "text", // Initial type
  name: "moderators", // Initial name
});

// Submit handler
const onSubmit = handleSubmit(async (values) => {
  if (props.group) {
    await props.updateGroupUtil({ ...values, id: props.supplier.id });
    return;
  }
  await props.addGroupUtil(values);
});
</script>
