<template>
  <table class="container mx-auto my-3 divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ID
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          EMAIL
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          USERNAME
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ROLE
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          CREATED AT
        </th>
        <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
          ACTIONS
        </th>
      </tr>
    </thead>

    <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="user in allUsers" :key="user.id">
        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
          {{ user.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.email }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.username }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.role }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ user.created_at }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
          <a href="#" class="text-indigo-600 hover:text-indigo-900">Edit</a>
        </td>
      </tr>
    </tbody>

  </table>
  <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Admin User Page
      </h2>
    </div>
  </div>
</template>
  
<script setup>
import { onMounted, computed, ref } from "vue";
import { useUser } from "../../store/user";

const user = useUser();

const allUsers = computed(() => {
  return user.getUsers;
});

onMounted(() => {
  user.getUsersAction();
});
</script>
  