<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/lib/supabaseClient'

const router = useRouter()
const user = ref<{ email?: string } | null>(null)
const loading = ref(false)

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

const goToChoice = () => {
  router.push({ name: 'choice' })
}

const handleSignOut = async () => {
  loading.value = true
  const { error } = await supabase.auth.signOut()
  loading.value = false

  if (error) {
    alert(error.message || 'Erro ao deslogar. Tente novamente.')
    return
  }

  router.replace({ name: 'login' })
}

onMounted(loadSession)
</script>

<template>
  <section class="min-h-screen bg-[#C9BEFF] text-slate-800 flex items-center justify-center">
    <div class="max-w-6xl w-full mx-auto px-4 py-12 flex flex-col items-center">
      <header class="flex flex-col items-center text-center gap-6 mb-12 w-full">
        <div class="flex flex-col items-center">
          <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight">Bem-vindo(a), <span class="text-blue-700">{{ userName }}</span></h1>
          <p class="mt-3 text-lg text-slate-800 font-semibold">Sua jornada de cuidar e crescer começa aqui.</p>
        </div>
        <button
          @click="handleSignOut"
          :disabled="loading"
          class="bg-white border-2 border-slate-200 text-slate-700 hover:bg-slate-50 hover:border-slate-300 hover:text-slate-900 transition-all px-6 py-2.5 rounded-xl font-semibold shadow-sm focus:ring-4 focus:ring-slate-100 disabled:opacity-50 flex items-center gap-2"
        >
          <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
          {{ loading ? 'Saindo...' : 'Sair' }}
        </button>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-5xl">
        <article class="group relative rounded-3xl border border-slate-200 bg-white p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="mb-5 inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 group-hover:scale-110 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-3 tracking-tight">Minhas metas</h2>
          <p class="text-slate-600 leading-relaxed">Acompanhe suas metas de saúde e bem-estar em um só lugar.</p>
        </article>

        <article class="group relative rounded-3xl border border-slate-200 bg-white p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="mb-5 inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 group-hover:scale-110 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-3 tracking-tight">Registros</h2>
          <p class="text-slate-600 leading-relaxed">Veja seu histórico de atividades diárias e progresso ao longo do tempo.</p>
        </article>

        <article class="group relative rounded-3xl border border-slate-200 bg-white p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
          <div class="mb-5 inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 group-hover:scale-110 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 mb-3 tracking-tight">Suporte</h2>
          <p class="text-slate-600 leading-relaxed">Acesse dicas e recursos para manter sua rotina saudável.</p>
        </article>
      </div>

      <div class="mt-12 w-full max-w-5xl relative overflow-hidden bg-white rounded-3xl p-10 border border-slate-200 shadow-[0_8px_30px_rgb(0,0,0,0.04)] text-center flex flex-col items-center">
        <!-- Decoration background glow -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-indigo-50/50 pointer-events-none"></div>
        
        <div class="relative z-10 max-w-2xl mx-auto">
          <h3 class="text-3xl font-extrabold text-slate-900 mb-4 tracking-tight">Pronto para começar?</h3>
          <p class="text-lg text-slate-600 leading-relaxed mb-8">Navegue entre as seções, personalize seus objetivos e acompanhe seu progresso com consistência.</p>
          <button @click="goToChoice" class="inline-flex items-center justify-center px-8 py-4 text-base font-bold text-white transition-all duration-200 bg-blue-600 border border-transparent rounded-xl hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 shadow-lg hover:shadow-blue-500/30 hover:-translate-y-0.5">
            Ir para escolha de perfil
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 ml-2 -mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>
