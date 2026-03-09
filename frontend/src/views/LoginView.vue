<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'
import leafLogo from '@/assets/leaf-svgrepo-com.svg'

const email = ref('')
const password = ref('')
const loading = ref(false)

const handleLogin = async () => {
  if (!email.value || !password.value) {
    alert('Por favor, preencha todos os campos.')
    return
  }

  loading.value = true
  try {
    const response = await fetch('http://localhost:3000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('token', data.token)
      localStorage.setItem('user', JSON.stringify(data.user))
      alert('Login realizado com sucesso!')
      // Here you would typically redirect to the dashboard
      // router.push('/dashboard');
    } else {
      alert(data.message || 'Erro ao realizar login')
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

        <div class="mt-8 text-center pt-6 border-t border-slate-50">
          <p class="text-slate-500 text-sm">
            Não tem uma conta?
            <a
              href="#"
              class="font-semibold text-primary-600 hover:text-primary-700 transition-colors ml-1"
              >Crie agora</a
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
