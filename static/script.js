const register = document.getElementById('registerDiv');
const login = document.getElementById('loginDiv');
const forgotpwd = document.getElementById('forgotDiv');

const reglink = document.getElementById('register');
const pwdlink = document.getElementById('pwd');
const authReq = document.getElementById('authentication');
const otpReq = document.getElementById('requestOTP')

reglink.addEventListener('click', function(){
    login.style.display = 'none';
    forgotpwd.style.display = 'none';
    register.style.display = 'flex';
});

pwdlink.addEventListener('click', function(){
    login.style.display = 'none';
    register.style.display = 'none';
    forgotpwd.style.display = 'flex';
    authReq.style.display = 'none';
});