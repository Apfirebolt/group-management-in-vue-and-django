<template>
    <div>
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-2 text-center text-3xl font-extrabold text-gray-900">
          Update Role
        </h2>
      </div>
  
      <div class="mt-4 sm:mx-auto sm:w-full sm:max-w-md">
        <div class="bg-white p-4 sm:rounded-lg sm:px-10">
          <form class="space-y-6" @submit="onSubmit">
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700">
                Role
              </label>
              <div class="mt-1">
                <input
                  id="email"
                  v-bind="roleAttributes"
                  v-model="role"
                  name="role"
                  type="text"
                  placeholder="Enter User Role"
                  class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </div>
              <p class="my-2 text-red-800">
                {{ errors.role }}
              </p>
            </div>
  
            <div>
              <button
                type="submit"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Update Role
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { computed } from "vue";
  import { useAuth } from "../store/auth";
  import { useForm } from "vee-validate";
  
  const auth = useAuth();
  
  // Validation, or use `yup` or `zod`
  function required(value) {
    return value ? true : "This field is required";
  }

  // Create the form
  const { defineField, handleSubmit, errors } = useForm({
    validationSchema: {
      role: required,
    },
  });
  
  // Define fields
  const [role, roleAttributes] = defineField("role", {
    type: "email", // Initial type
    name: "email", // Initial name
  });
  
  // Submit handler
  const onSubmit = handleSubmit(async (values) => {
    // Submit to API
    await auth.loginAction(values);
  });
  </script>
  