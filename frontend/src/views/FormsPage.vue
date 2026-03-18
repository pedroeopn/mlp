<template>
  <section class="min-h-screen bg-slate-50 flex items-center justify-center p-4">
    <div class="w-full max-w-2xl bg-white rounded-3xl shadow-xl border border-slate-100 p-8 md:p-12">
      <div class="text-center mb-10">
        <h1 class="text-3xl md:text-4xl font-extrabold text-slate-900 mb-3 tracking-tight">Cadastro de Cuidador</h1>
        <p class="text-lg text-slate-600">Preencha o formulário abaixo para fazer parte da nossa rede de cuidadores.</p>
      </div>

      <form class="space-y-6">
        <div class="space-y-1">
          <label class="block text-sm font-semibold text-slate-700">Nome Completo</label>
          <input type="text" class="w-full border-2 border-slate-200 bg-slate-50 rounded-xl p-3 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium" placeholder="Ex: Maria da Silva" />
        </div>
        
        <fieldset class="space-y-3 p-4 border-2 border-slate-200 rounded-xl bg-slate-50">
          <legend class="text-sm font-semibold text-slate-700 px-2 -ml-2">Gênero</legend>
          <div class="flex gap-6">
            <label class="inline-flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sexo" value="feminino" class="w-5 h-5 text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer" />
              <span class="text-slate-700 font-medium group-hover:text-slate-900 transition-colors">Feminino</span>
            </label>
            <label class="inline-flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sexo" value="masculino" class="w-5 h-5 text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer" />
              <span class="text-slate-700 font-medium group-hover:text-slate-900 transition-colors">Masculino</span>
            </label>
            <label class="inline-flex items-center gap-2 cursor-pointer group">
              <input type="radio" name="sexo" value="outro" class="w-5 h-5 text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer" />
              <span class="text-slate-700 font-medium group-hover:text-slate-900 transition-colors">Outro</span>
            </label>
          </div>
        </fieldset>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-slate-700">Idade</label>
          <input type="tel" class="w-full border-2 border-slate-200 bg-slate-50 rounded-xl p-3 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium" placeholder="Sua idade" />
        </div>

        <div class="space-y-1">
          <label class="block text-sm font-semibold text-slate-700">Cursos e experiências</label>
          <textarea rows="4" class="w-full border-2 border-slate-200 bg-slate-50 rounded-xl p-3 text-slate-900 placeholder-slate-400 focus:bg-white focus:outline-none focus:ring-4 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium resize-none" placeholder="Conte um pouco sobre os cursos que realizou e sua experiência..."></textarea>
        </div>


        <div class="pt-4 mt-8 border-t border-slate-100 flex justify-end">
          <button type="submit" class="w-full sm:w-auto px-8 py-3.5 bg-blue-600 text-white rounded-xl font-bold shadow-md shadow-blue-500/30 hover:bg-blue-700 hover:-translate-y-0.5 focus:outline-none focus:ring-4 focus:ring-blue-500/50 transition-all flex items-center justify-center gap-2">
             <span>Enviar Cadastro</span>
             <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
               <path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
             </svg>
          </button>
        </div>
      </form>
    </div>
  </section>
</template>
