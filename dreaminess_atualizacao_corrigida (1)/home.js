(async function(){
 const container=document.querySelector('#textos');if(!container)return;
 try{
  const response=await fetch('posts.json',{cache:'no-cache'});if(!response.ok)throw new Error('Sem índice');
  const posts=await response.json();if(!Array.isArray(posts)||!posts.length)return;
  container.replaceChildren();
  for(const post of posts){
   const article=document.createElement('article');article.className='article-preview';
   const eyebrow=document.createElement('div');eyebrow.className='eyebrow';eyebrow.textContent=post.date?`Reflexões · ${post.date}`:'Reflexões';article.appendChild(eyebrow);
   const h2=document.createElement('h2'),link=document.createElement('a');link.href=post.url;link.textContent=post.title;h2.appendChild(link);article.appendChild(h2);
   if(post.image){const figure=document.createElement('figure');figure.className='cover';const img=document.createElement('img');img.src=post.image;img.alt=post.imageAlt||'';img.loading='lazy';figure.appendChild(img);article.appendChild(figure)}
   if(post.description){const p=document.createElement('p');p.textContent=post.description;article.appendChild(p)}
   const read=document.createElement('a');read.className='read';read.href=post.url;read.textContent='Ler texto →';article.appendChild(read);container.appendChild(article)
  }
 }catch(e){console.warn('Mantendo prévia original:',e)}
})();
