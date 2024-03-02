<template>
  <table class="container mx-auto my-3 divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          ID
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          GROUP NAME
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          USER NAME
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          STATUS
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          CREATED AT
        </th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      <tr v-for="groupTask in getGroupTasks" :key="groupTask.id">
        <td
          class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900"
        >
          {{ groupTask.id }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ groupTask.group_name }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ groupTask.user_name }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ groupTask.status }}
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ groupTask.created_at }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script setup>

const props = defineProps({
    getGroupTasks: {
        type: Array,
        required: true,
    },
});
</script>
