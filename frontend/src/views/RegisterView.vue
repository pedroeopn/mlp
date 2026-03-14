<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import leafLogo from '@/assets/leaf-svgrepo-com.svg'
import { supabase } from '@/lib/supabaseClient'

const router = useRouter()
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)

const handleRegister = async () => {
  if (!email.value || !password.value || !confirmPassword.value) {
    alert('Por favor, preencha todos os campos.')
    return
  }

  if (password.value !== confirmPassword.value) {
    alert('As senhas não coincidem.')
    return
  }

  loading.value = true
  try {
    const { data, error } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
    })

    if (error) {
      alert(error.message || 'Erro ao realizar o cadastro')
      return
    }

    if (data.user) {
      alert('Cadastro realizado com sucesso! Verifique seu e-mail, se necessário, ou faça login.')
      router.push('/')
    }
  } catch (error) {
    console.error('Registration error:', error)
    alert('Erro de conexão com o servidor')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div
    class="min-h-screen flex items-center justify-center bg-slate-50 p-6 selection:bg-primary-100 selection:text-primary-900"
  >
    <div class="w-full max-w-md">
      <!-- Logo/Brand Section -->
      <div class="text-center mb-10">
        <div
          class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary-600 text-white shadow-xl shadow-primary-600/20 mb-4 transform hover:rotate-12 transition-transform duration-300"
        >
          <img :src="leafLogo" alt="CuidarBem Logo" class="h-10 w-10" />
        </div>
        <h1 class="text-3xl font-bold text-slate-900 tracking-tight">CuidarBem</h1>
        <p class="text-slate-500 mt-2">Crie sua conta para começar</p>
      </div>

      <div class="pt-2"></div>

      <!-- Register Card -->
      <div
        class="bg-white p-8 pt-2 rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100"
      >
        <form @submit.prevent="handleRegister" class="space-y-6">
          <BaseInput
            id="email"
            label="E-mail"
            v-model="email"
            type="email"
            placeholder="seu@email.com"
          />

          <BaseInput
            id="password"
            label="Senha"
            v-model="password"
            type="password"
            placeholder="••••••••"
          />

          <BaseInput
            id="confirmPassword"
            label="Confirmar Senha"
            v-model="confirmPassword"
            type="password"
            placeholder="••••••••"
          />

          <div class="pt-2">
            <BaseButton type="submit" :loading="loading"> Criar Conta </BaseButton>
          </div>
        </form>

        <div class="mt-8 text-center pt-6 border-t border-slate-50">
          <p class="text-slate-500 text-sm">
            Já tem uma conta?
            <RouterLink
              to="/"
              class="font-semibold text-primary-600 hover:text-primary-700 transition-colors ml-1"
            >
              Faça login agora!
            </RouterLink>
          </p>
        </div>
      </div>

      <!-- Footer Help -->
      <p class="text-center text-slate-400 text-sm mt-10">
        &copy; 2026 CuidarBem. Todos os direitos reservados.
      </p>
    </div>
  </div>
</template>
