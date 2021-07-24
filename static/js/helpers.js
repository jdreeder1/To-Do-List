const menu_toggle = document.getElementById('menu_toggle');
const nav_link = document.getElementById('nav_links');
const nav_btns = nav_link.querySelectorAll('button');
const close_btn = document.getElementById('close');

menu_toggle.addEventListener('click', ()=> {
    //nav_link.classList.toggle('toggle');
    nav_btns.forEach(btn=> { btn.classList.add('open'); });
    menu_toggle.style.display = 'none';
    close_btn.style.display = 'block';
    //console.log('clicked!');
});
close_btn.addEventListener('click', ()=> {
    nav_btns.forEach(btn=> { btn.classList.remove('open'); });
    menu_toggle.style.display = 'block';
    close_btn.style.display = 'none';
});

window.addEventListener('resize', ()=> {
    if (window.matchMedia("(min-width: 901px)").matches) {
        menu_toggle.style.display = 'none';
        close_btn.style.display = 'none';
    }
    else {
        menu_toggle.style.display = 'block'; 
    }
});