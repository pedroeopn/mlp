<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import { supabase } from '@/lib/supabaseClient'

const router = useRouter()
const user = ref<{ email?: string } | null>(null)

const userName = computed(() => {
  if (!user.value?.email) return 'Usuário'
  return user.value.email.split('@')[0]
})

const loadSession = async () => {
  const { data } = await supabase.auth.getSession()
  if (!data.session) {
    router.replace({ name: 'login' })
    return
  }
  user.value = data.session.user
}

onMounted(loadSession)

const goToRegister = () => router.push({ name: 'forms-page' })
const goToFindCaregiver = () => router.push({ name: 'found-caregiver' })
</script>

<template>
  <section class="min-h-screen bg-white flex items-center justify-center">
    <div class="w-full max-w-4xl p-6">
      <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-10">Bem-vindo, {{ userName }}</h1>
      <p class="text-lg text-slate-700 mb-8">Escolha uma das opções para continuar.</p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="rounded-3xl border border-slate-200 bg-white shadow-sm p-6">
          <h2 class="text-xl font-bold text-slate-800 mb-2">É um cuidador?</h2>
          <p class="text-slate-600 mb-4">Se cadastre agora</p>
          <BaseButton @click="goToRegister">Cadastrar como cuidador</BaseButton>
        </div>
        <div class="rounded-3xl border border-slate-200 bg-white shadow-sm p-6">
          <h2 class="text-xl font-bold text-slate-800 mb-2">Procurando um cuidador</h2>
          <p class="text-slate-600 mb-4">Encontre o melhor perfil para você</p>
          <BaseButton @click="goToFindCaregiver">Buscar cuidador</BaseButton>
        </div>
      </div>
    </div>
  </section>
</template>
