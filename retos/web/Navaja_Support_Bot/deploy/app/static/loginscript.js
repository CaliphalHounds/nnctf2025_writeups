        const loginTab = document.getElementById('loginTab');
        const registerTab = document.getElementById('registerTab');
        const actionInput = document.getElementById('actionInput');
        const submitBtn = document.getElementById('submitBtn');

        loginTab.onclick = () => {
            loginTab.classList.add('active');
            registerTab.classList.remove('active');
            actionInput.value = 'login';
            submitBtn.textContent = 'Login';
        }

        registerTab.onclick = () => {
            registerTab.classList.add('active');
            loginTab.classList.remove('active');
            actionInput.value = 'register';
            submitBtn.textContent = 'Register';
       }
