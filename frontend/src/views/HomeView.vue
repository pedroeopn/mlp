<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '@/lib/supabaseClient'
import BaseButton from '@/components/BaseButton.vue'

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
  <section class="min-h-screen bg-gradient-to-br from-primary-100 to-sky-50 text-slate-800">
    <div class="max-w-6xl mx-auto px-4 py-12">
      <header class="flex flex-col md:flex-row md:items-center md:justify-between gap-6 mb-10">
        <div>
          <h1 class="text-4xl md:text-5xl font-extrabold text-primary-800">Bem-vindo(a), {{ userName }}</h1>
          <p class="mt-2 text-lg text-slate-700">Sua jornada de cuidar e crescer começa aqui.</p>
        </div>
        <button
          @click="handleSignOut"
          :disabled="loading"
          class="bg-primary-600 text-white hover:bg-primary-700 transition-colors px-5 py-2.5 rounded-lg font-semibold shadow-md disabled:opacity-50"
        >
          {{ loading ? 'Saindo...' : 'Sair' }}
        </button>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <article class="rounded-2xl border border-primary-100 bg-white p-6 shadow-sm hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-bold text-primary-700 mb-2">Minhas metas</h2>
          <p class="text-slate-600">Acompanhe suas metas de saúde e bem-estar em um só lugar.</p>
        </article>

        <article class="rounded-2xl border border-primary-100 bg-white p-6 shadow-sm hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-bold text-primary-700 mb-2">Registros</h2>
          <p class="text-slate-600">Veja seu histórico de atividades diárias e progresso ao longo do tempo.</p>
        </article>

        <article class="rounded-2xl border border-primary-100 bg-white p-6 shadow-sm hover:shadow-lg transition-shadow">
          <h2 class="text-xl font-bold text-primary-700 mb-2">Suporte</h2>
          <p class="text-slate-600">Acesse dicas e recursos para manter sua rotina saudável.</p>
        </article>
      </div>

      <div class="mt-10 bg-white rounded-2xl p-8 border border-slate-100 shadow-sm">
        <h3 class="text-2xl font-bold text-primary-800 mb-3">Pronto para começar?</h3>
        <p class="text-slate-700">Navegue entre as seções, personalize seus objetivos e acompanhe seu progresso com consistência.</p>
        <BaseButton @click="goToChoice" class="mt-6">
          Ir para escolha de perfil
        </BaseButton>
      </div>
    </div>
  </section>
</template>
