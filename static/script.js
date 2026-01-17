const register = document.getElementById('registerDiv');
const login = document.getElementById('loginDiv');

const reglink = document.getElementById('register');

reglink.addEventListener('click', function(){
    login.style.display = 'none';
    register.style.display = 'flex';
});
