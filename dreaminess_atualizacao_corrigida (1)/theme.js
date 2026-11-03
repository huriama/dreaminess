(function(){
  const key='dreaminess-theme';
  let saved=null;
  try{saved=localStorage.getItem(key)}catch(e){}
  const initial=saved==='dark'||saved==='light'?saved:(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
  document.documentElement.dataset.theme=initial;
  function update(){document.querySelectorAll('.theme-toggle').forEach(button=>{const dark=document.documentElement.dataset.theme==='dark';button.textContent=dark?'☀':'☾';button.setAttribute('aria-label',dark?'Ativar modo claro':'Ativar modo noturno');button.setAttribute('title',dark?'Ativar modo claro':'Ativar modo noturno')})}
  document.addEventListener('DOMContentLoaded',()=>{
    if(!document.querySelector('.theme-toggle')){
      const header=document.querySelector('header');
      if(header){const button=document.createElement('button');button.type='button';button.className='theme-toggle';header.appendChild(button)}
    }
    update();
    document.querySelectorAll('.theme-toggle').forEach(button=>button.addEventListener('click',()=>{const next=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=next;try{localStorage.setItem(key,next)}catch(e){}update()}));
  });
})();
