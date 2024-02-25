<template>
  <div class="sm:mx-auto sm:w-full sm:max-w-md">
    <div class="bg-white p-4 sm:rounded-lg sm:px-10">
      <h2 class="my-4 text-center text-xl font-extrabold text-gray-900">
        Confirm
      </h2>
      <form class="space-y-6" @submit="onSubmit">
        <p>
          {{ message }}
        </p>

        <div class="flex justify-between">
          <button
            type="button"
            @click="cancelAction"
            class="bg-red-500 hover:bg-red-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-700 active:bg-blue-800 px-4 py-2 rounded text-white font-bold mx-1"
          >
            Confirm
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  message: {
    type: String,
    required: true,
  },
  confirmAction: {
    type: Function,
    required: true,
  },
  cancelAction: {
    type: Function,
    required: true,
  },
});

// Submit handler
const onSubmit = async () => {
  await props.confirmAction();
};
</script>
