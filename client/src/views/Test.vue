<template>
    <div class="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          A Test Page
        </h2>
      </div>
      
      <button @click="anotherFunction" class="px-2 py-1 bg-orange-300 rounded shadow-md hover:bg-orange-700 hover:text-white transition-all">
        Click Wait
      </button>

    </div>
  </template>
  
  <script setup>
  import { computed, ref } from "vue";
  import httpClient
   from "../plugins/interceptor";
  // Submit handler
  const onClick = async () => {
    console.log("Clicked");
    // const response = httpClient.get('suppliers')
    const response = await new Promise((resolve, reject) => {
      setTimeout(() => {
        const response = httpClient.get('suppliers');
        reject("Has some error")
        response.then((res) => {
          console.log("Response nested", res);
          resolve(res);
        });
      }, 3000);
    });
    return response;
  };

  const anotherFunction = async () => {
    console.log("Another function");
    const p = onClick();
    p.then((res) => {
      console.log("Response", res);
    })
    .catch((err) => {
      console.log("Has some Error caught", err);
    });
    console.log("After await");
  };

  
  </script>
  