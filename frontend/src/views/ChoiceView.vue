<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
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
  <section class="min-h-screen bg-slate-50 flex items-center justify-center p-4">
    <!-- Background subtle gradient -->
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-blue-50 via-slate-50 to-slate-50 pointer-events-none"></div>
    
    <div class="w-full max-w-4xl relative z-10 flex flex-col items-center mx-auto">
      <div class="text-center mb-12 flex flex-col items-center">
        <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-4 tracking-tight">Bem-vindo, <span class="text-blue-600">{{ userName }}</span></h1>
        <p class="text-lg text-slate-600 font-medium text-center">Escolha uma das opções abaixo para continuar a sua jornada.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-3xl w-full mx-auto">
        <!-- Card 1: Cuidador -->
        <div 
          @click="goToRegister"
          class="group cursor-pointer rounded-3xl border-2 border-transparent bg-white shadow-lg hover:shadow-xl hover:border-blue-200 hover:-translate-y-1 transition-all duration-300 p-8 flex flex-col items-center text-center"
        >
          <div class="w-20 h-20 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-blue-600 group-hover:text-white transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-2">Sou um Cuidador</h2>
          <p class="text-slate-600 mb-8 leading-relaxed">Cadastre seu perfil, ofereça seus serviços e encontre oportunidades de trabalho.</p>
          <button class="w-full mt-auto bg-slate-100 text-slate-700 font-bold py-3 px-6 rounded-xl group-hover:bg-blue-50 group-hover:text-blue-700 transition-colors">
            Cadastrar-se
          </button>
        </div>

        <!-- Card 2: Procurando Cuidador -->
        <div 
          @click="goToFindCaregiver"
          class="group cursor-pointer rounded-3xl border-2 border-transparent bg-white shadow-lg hover:shadow-xl hover:indigo-200 hover:-translate-y-1 transition-all duration-300 p-8 flex flex-col items-center text-center"
        >
          <div class="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-indigo-600 group-hover:text-white transition-all duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-2">Busco um Cuidador</h2>
          <p class="text-slate-600 mb-8 leading-relaxed">Encontre o profissional ideal para atender às suas necessidades com segurança.</p>
          <button class="w-full mt-auto bg-slate-100 text-slate-700 font-bold py-3 px-6 rounded-xl group-hover:bg-indigo-50 group-hover:text-indigo-700 transition-colors">
            Encontrar profissionais
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
