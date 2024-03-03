<template>
    <table v-if="getGroupQueues.length" class="container mx-auto my-3 divide-y divide-gray-200">
        <thead class="bg-gray-50">
            <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    ID
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    GROUP NAME
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    USER NAME
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    STATUS
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    CREATED AT
                </th>
            </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="groupQueue in getGroupQueues" :key="groupQueue.id">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {{ groupQueue.id }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ groupQueue.group_name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ groupQueue.user_name }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span class="px-3 py-2 rounded-full text-white font-bold shadow-md m-1" :class="[groupQueue.admin_approved ? 'bg-green-500' : 'bg-orange-300']">
                        {{ groupQueue.admin_approved ? 'Approved' : 'Pending'}}
                    </span>
                    <span class="px-3 py-2 rounded-full text-white font-bold shadow-md m-1" :class="[groupQueue.moderator_approved ? 'bg-green-500' : 'bg-orange-300']">
                        {{ groupQueue.moderator_approved ? 'Approved' : 'Pending'}}
                    </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {{ formatDate(groupQueue.created_at) }}
                </td>
            </tr>
        </tbody>
    </table>
    <div v-else class="text-center text-gray-500">
        <p>
            No group queues found
        </p>
    </div>
</template>

<script setup>
import dayjs from 'dayjs';

const props = defineProps({
    getGroupQueues: {
        type: Array,
        required: true,
    },
});

const formatDate = (date) => {
    return dayjs(date).format('MMMM D, YYYY');
};
</script>
