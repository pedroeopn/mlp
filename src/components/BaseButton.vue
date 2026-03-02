<script setup lang="ts">
defineProps<{
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
}>();
</script>

<template>
  <button
    :type="type || 'button'"
    :disabled="loading"
    class="w-full relative overflow-hidden group px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl transition-all duration-300 transform active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed shadow-lg shadow-primary-600/20 hover:shadow-primary-600/40"
  >
    <div class="absolute inset-0 w-3 bg-white/20 transition-all duration-500 -skew-x-12 -translate-x-10 group-hover:translate-x-[400px]"></div>
    
    <span v-if="!loading" class="relative flex items-center justify-center gap-2">
      <slot />
    </span>
    
    <span v-else class="relative flex items-center justify-center">
      <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
  </button>
</template>
