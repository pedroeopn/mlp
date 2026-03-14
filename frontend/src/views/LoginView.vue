<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import leafLogo from '@/assets/leaf-svgrepo-com.svg'
import { supabase } from '@/lib/supabaseClient'

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleGoogleLogin = async () => {
  try {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
    })
    
    if (error) {
      alert(error.message || 'Erro ao realizar login com Google')
    }
  } catch (error) {
    console.error('Google login error:', error)
    alert('Erro de conexão com o servidor')
  }
}

const handleLogin = async () => {
  if (!email.value || !password.value) {
    alert('Por favor, preencha todos os campos.')
    return
  }

  loading.value = true
  try {
    const { data, error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    })

    if (error) {
      alert(error.message || 'Erro ao realizar login')
      return
    }

    if (data.session) {
      // Supabase handles session storage in localStorage automatically
      alert('Login realizado com sucesso!')
      // Here you would typically redirect to the dashboard
      // router.push('/dashboard');
    }
  } catch (error) {
    console.error('Login error:', error)
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
        <p class="text-slate-500 mt-2">Acesse sua conta para continuar</p>
      </div>

      <!-- Login Card -->
      <div class="bg-white p-8 rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <BaseInput
            id="email"
            label="E-mail"
            v-model="email"
            type="email"
            placeholder="seu@email.com"
          />

          <div class="space-y-1">
            <BaseInput
              id="password"
              label="Senha"
              v-model="password"
              type="password"
              placeholder="••••••••"
            />
            <div class="flex justify-end">
              <a
                href="#"
                class="text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
                >Esqueceu a senha?</a
              >
            </div>
          </div>

          <BaseButton type="submit" :loading="loading"> Entrar </BaseButton>
        </form>

        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-slate-200"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-slate-500">ou continue com</span>
            </div>
          </div>

          <div class="mt-6">
            <button
              @click="handleGoogleLogin"
              type="button"
              class="w-full inline-flex justify-center items-center py-2.5 px-4 border border-slate-300 rounded-lg shadow-sm bg-white text-sm font-medium text-slate-700 hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors"
            >
              <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Google
            </button>
          </div>
        </div>

        <div class="mt-8 text-center pt-6 border-t border-slate-50">
          <p class="text-slate-500 text-sm">
            Não tem uma conta?
            <RouterLink
              to="/register"
              class="font-semibold text-primary-600 hover:text-primary-700 transition-colors ml-1"
              >Crie agora</RouterLink
            >
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
