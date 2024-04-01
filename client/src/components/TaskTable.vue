<template>
  <table v-if="getGroupTasks && getGroupTasks.length" class="container mx-auto my-3 divide-y divide-gray-200">
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
          ASSIGNED TO
        </th>
        <th
          scope="col"
          class="px-6 col-span-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          STATUS
        </th>
        <th
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          CREATED AT
        </th>
        <th
          v-if="dashboardView"
          scope="col"
          class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
        >
          ACTIONS
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
          <span class="px-3 py-2 rounded-full text-white font-bold shadow-md" :class="[groupTask.status ? 'bg-green-500' : 'bg-orange-300']">
            {{ groupTask.status ? 'Approved' : 'Pending'}}
          </span>
        </td>
        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
          {{ formatDate(groupTask.created_at) }}
        </td>
        <td
          v-if="dashboardView"
          class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        >
          <button
            @click="approveTask({ id: groupTask.id, status: true })"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-1"
          >
            Approve
          </button>
          <button
            @click="approveTask({ id: groupTask.id, status: false })"
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded m-1"
          >
            Reject
          </button>
        </td>
      </tr>
    </tbody>
  </table>
  <div v-else class="text-center text-gray-500">
        <p>
            No group tasks found
        </p>
    </div>
</template>

<script setup>
import dayjs from 'dayjs';

const props = defineProps({
  getGroupTasks: {
    type: Array,
    required: true,
  },
  dashboardView: {
    type: Boolean,
    required: false,
  },
  approveTask: {
    type: Function,
    required: false,
  },
});

const formatDate = (date) => dayjs(date).format('YYYY-MM-DD');

</script>