<template>
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white p-4 sm:rounded-lg sm:px-10">
          <h2 class="my-4 text-center text-xl font-extrabold text-gray-900">
              {{ category ? 'Update Category' : 'Add Category' }}
          </h2>
        <form class="space-y-6" @submit="onSubmit">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">
              Category Name
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
            <button
              type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              {{ category ? 'Update Category' : 'Add Category' }}
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
      category: {
          type: Object,
          required: false,
      },
      addCategoryUtil: {
          type: Function,
          required: true,
      },
      updateCategoryUtil: {
          type: Function,
          required: true,
      },
  });
  
  onMounted(() => {
      if (props.category) {
          name.value = props.category.name;
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
    },
  });
  
  // Define fields
  const [name, nameAttributes] = defineField("name", {
    type: "text", // Initial type
    name: "name", // Initial name
  });
  
  // Submit handler
  const onSubmit = handleSubmit(async (values) => {
      if (props.category) {
          await props.updateCategoryUtil({ ...values, id: props.category.id });
          return;
      }
      await props.addCategoryUtil(values);
  });
  </script>
  