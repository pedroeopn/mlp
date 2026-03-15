<template>
  <section class="min-h-screen bg-white flex items-center justify-center">
    <div class="w-full max-w-4xl p-6">
      <h1 class="text-4xl md:text-5xl font-extrabold text-slate-900 mb-8">Cadastro de Cuidador</h1>
      <p class="text-lg text-slate-700 mb-6">Preencha o formulário para se cadastrar como cuidador.</p>

      <form class="space-y-4 bg-white border border-slate-200 p-6 rounded-2xl shadow-sm">
        <label class="block">
          <span class="text-slate-700">Nome Completo</span>
          <input type="text" class="mt-1 block w-full border border-slate-300 rounded-lg p-2" placeholder="Seu nome" />
        </label>
        <fieldset class="space-y-2">
          <legend class="text-slate-700">Sexo</legend>
          <label class="inline-flex items-center gap-2">
            <input type="radio" name="sexo" value="feminino" class="text-blue-600 focus:ring-blue-500" />
            <span class="text-slate-700">Feminino</span>
          </label>
          <label class="inline-flex items-center gap-2">
            <input type="radio" name="sexo" value="masculino" class="text-blue-600 focus:ring-blue-500" />
            <span class="text-slate-700">Masculino</span>
          </label>
        </fieldset>
        <label class="block">
          <span class="text-slate-700">Idade</span>
          <input type="tel" class="mt-1 block w-full border border-slate-300 rounded-lg p-2" placeholder="Sua idade" />
        </label>
        <label class="block">
          <span class="text-slate-700">Cursos e experiências</span>
          <input type="tel" class="mt-1 block w-full border border-slate-300 rounded-lg p-2" placeholder="Conte um pouco sobre os cursos que realizou e sua experiência, quanto mais detalhes, melhor!" />
        </label>


        <div class="flex justify-end">
          <button type="submit" class="px-5 py-2.5 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors">Enviar</button>
        </div>
      </form>
    </div>
  </section>
</template>
